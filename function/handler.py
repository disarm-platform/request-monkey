from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
from os import sys
import os
from pathlib import Path
import time
import re
import urllib.request
from threading import Thread
from socket import timeout
import random

base_url = 'https://faas.srv.disarm.io/function/'
HEADERS = {
    'accept': 'application/json'
}


class GetUrlThread(Thread):
    def __init__(self, function_name):
        self.function_name = function_name
        self.result = {}
        super(GetUrlThread, self).__init__()

    def run(self):
        resp = test_function(self.function_name)
        self.result = resp


def load_as_json(contents):
    try:
        obj = json.load(contents)
        return obj
    except OSError:
        print("Could parse", contents + 'as json')
        sys.exit()


def get_test_req(function_name):
    try:
        cwd = os.getcwd()
        contents = ''
        with open(os.path.join(cwd, 'function', 'test_reqs', function_name + '.json'), 'r', newline=None) as f:
            contents = load_as_json(f)
        return contents
    except OSError:
        print("Could not open/read file:" + os.path.join(cwd,
                                                         'function', 'test_reqs', function_name + '.json'))
        sys.exit()


def send_request(function_name, d):
    request = Request(base_url + function_name, data=d, headers=HEADERS)
    r = {"function_name": function_name, "code": "",
         "reason": "something went wrong", "execution_time": ""}
    start_time = time.time()
    try:
        response = urlopen(request, timeout=30)
        r["code"] = response.getcode()
        r["reason"] = "function works as expected"
    except HTTPError as e:
        if hasattr(e, 'reason'):
            r["reason"] = e.reason
        if hasattr(e, 'code'):
            r["code"] = e.code
    except timeout:
        r["reason"] = "timeout"
    r["execution_time"] = time.time() - start_time
    return r


def test_function(name):
    test_req_file = get_test_req(name)
    json_content = test_req_file
    return send_request(name, d=json_content.encode())


def test_random_func():
    fileNames = get_all_filenames()
    return test_function(random.choice(fileNames))


def get_all_filenames():
    dirName = os.path.join(os.getcwd(), 'function', 'test_reqs')
    fileNames = [f.split('.')[0] for f in os.listdir(
        dirName) if os.path.isfile(os.path.join(dirName, f))]
    return fileNames


def test_all():
    fileNames = get_all_filenames()
    threads = []
    for f in fileNames:
        t = GetUrlThread(f)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    result = []
    for t in threads:
        result.append(t.result)
    return result


def handle(params: dict):
    if "base_url" in params:
        base_url = params.get(base_url, base_url)
    if "all" in params:
        return test_all()
    elif "random" in params:
        return test_random_func()
    elif "function_name" in params:
        return test_function(params.get("function_name"))
