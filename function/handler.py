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

default_base_url = 'https://faas.srv.disarm.io/function/'
HEADERS = {'accept': 'application/json'}


class GetUrlThread(Thread):
    def __init__(self, base_url, function_name):
        self.base_url = base_url
        self.function_name = function_name
        self.result = {}
        super(GetUrlThread, self).__init__()

    def run(self):
        resp = test_function(self.base_url, self.function_name)
        self.result = resp


def load_as_json(contents):
    try:
        obj = json.load(contents)
        return obj
    except OSError:
        print("Could parse", contents + 'as json')
        sys.exit()


# TODO: Replace with getting test_req from the repo
def get_test_req(function_name):
    try:
        cwd = os.getcwd()
        contents = ''
        with open(os.path.join(cwd, 'function', 'test_reqs',
                               function_name + '.json'),
                  'r',
                  newline=None) as f:
            contents = load_as_json(f)
        return contents
    except OSError:
        print("Could not open/read file:" +
              os.path.join(cwd, 'function', 'test_reqs', function_name +
                           '.json'))
        sys.exit()


def send_request(base_url, function_name, d):
    request = Request(base_url + function_name, data=d, headers=HEADERS)
    r = {
        "function_name": function_name,
        "code": "",
        "reason": "something went wrong",
        "execution_time": ""
    }
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


def test_function(base_url: str, name: str):
    test_req_file = get_test_req(name)
    json_content = test_req_file
    return send_request(base_url, name, d=json_content.encode())


def test_random_func(base_url: str):
    fileNames = get_all_filenames()
    random_choice = random.choice(fileNames)
    print(random_choice)
    return test_function(base_url, random_choice)


def get_all_filenames():
    dirName = os.path.join(os.getcwd(), 'function', 'test_reqs')
    fileNames = [
        f.split('.')[0] for f in os.listdir(dirName)
        if os.path.isfile(os.path.join(dirName, f))
    ]
    return fileNames


def test_all(base_url: str):
    fileNames = get_all_filenames()
    threads = []

    for fileName in fileNames:
        thread = GetUrlThread(base_url, fileName)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    result = []
    for thread in threads:
        result.append(thread.result)

    return result


def handle(params_raw: str):
    try:
        params = json.loads(params_raw)
    except json.decoder.JSONDecodeError:
        return "Invalid JSON provided as params"

    base_url = params.get('base_url', default_base_url)

    if "all" in params:
        return test_all(base_url)
    elif "random" in params:
        return test_random_func(base_url, )
    elif "function_name" in params:
        function_name = params.get("function_name")
        return test_function(base_url, function_name)
