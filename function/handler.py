from urllib.request import Request, urlopen
from urllib.error import  URLError
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

base_url = 'https://faas.srv3.disarm.io/function/'
HEADERS = {
    'accept': 'application/json'
}
    # print("Elapsed time: %s" % (time.time()-start))
# `run_function` receives `params` as a dict
# Return something which is serializable using `json.dumps()`

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
       with open(os.path.join(cwd,'function','test_reqs',function_name + '.json'), 'r', newline=None) as f:
            contents = load_as_json(f)
       return contents
    except OSError:
        print("Could not open/read file:" + os.path.join(cwd,'function','test_reqs',function_name + '.json'))
        sys.exit()


def send_request(function_name,d):
    request = Request(base_url + function_name,data=d,headers=HEADERS,)
    r = {"function_name": function_name, "code": "", "reason": "something went wrong", "execution_time":""}
    start_time = time.time()
    try:
        response = urlopen(request, timeout=30)
        r["code"] = response.getcode()
        r["reason"] = "function works as expected"
    except URLError as e:
        if hasattr(e, 'reason'):
            r["reason"] = e.reason
        elif hasattr(e, 'code'):
            r["code"] = e.code
    except timeout:
        r["reason"] = "timeout"
    r["execution_time"] = time.time() - start_time
    return r

def interpret_status_code(code):
    if re.search("^2([0-9]+){2}", code):
        return "function was successful"
    return "request failed!"

def get_function_info(name):
    test_req_file = get_test_req(name)
    json_content  = json.dumps(test_req_file)
    return send_request(name,d=json_content.encode())

class GetUrlThread(Thread):
    def __init__(self, function_name):
        self.function_name = function_name
        self.result = {}
        super(GetUrlThread, self).__init__()    

    def run(self):
        resp = get_function_info(self.function_name)
        self.result = resp

def test_random_func():
    fileNames = get_all_filenames()
    return get_function_info(random.choice(fileNames))
    


def get_all_filenames():
    dirName = os.path.join(os.getcwd(),'function','test_reqs')
    fileNames = [f.split('.')[0] for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]
    return fileNames

def get_responses():
    fileNames = get_all_filenames()
    threads = []
    start = time.time()
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

def run_function(params: dict):

    if params["all"]:
        return get_responses()
    elif params["random"]:
        return test_random_func()

    return get_function_info(params['function_name'])
