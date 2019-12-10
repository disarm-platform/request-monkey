from function.preprocess_params import preprocess
from function.preprocess_helpers import check_if_exists
from urllib.request import Request, urlopen
from urllib.error import  URLError
import json
from os import sys
import os
from pathlib import Path
# `run_function` receives `params` as a dict
# Return something which is serializable using `json.dumps()`

base_url = 'https://faas.srv.disarm.io/function/'
HEADERS = {
    'accept': 'application/json; utf-8'
    
}


def load_as_json(contents):
    try:
        obj = json.load(contents)
        return obj
    except OSError:
        print("Could parse", contents + 'as json')
        sys.exit()


def get_test_req(func_name):
    try:
       cwd = os.getcwd()
       contents = ''
       with open(os.path.join(cwd,'function','test_reqs',func_name + '.json'), 'r', newline=None) as f:
            contents = load_as_json(f)
       return contents
    except OSError:
        print("Could not open/read file:" + os.path.join(cwd,'function','test_reqs',func_name + '.json'))
        sys.exit()


def send_request(func_name,d):
    req = Request(base_url + func_name,data=d,headers=HEADERS)
    try:
        response = urlopen(req)
        return response.read().decode()
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)


def run_function(params: dict):
    preprocess(params)
    
    if check_if_exists('func_name', params):
        file = get_test_req(params["func_name"])
        json_d  = json.dumps(file)
        response = send_request(params["func_name"],d=json_d.encode())
        return response
    else:
        pass
