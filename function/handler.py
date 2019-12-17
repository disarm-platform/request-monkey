from function.preprocess_params import preprocess
from function.preprocess_helpers import check_if_exists
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

base_url = 'https://faas.srv3.disarm.io/function/'
HEADERS = {
    'accept': 'application/json'
}
class GetUrlThread(Thread):
    def __init__(self, func_name):
        self.func_name = func_name
        super(GetUrlThread, self).__init__()    

    def run(self):
        resp = get_function_info(self.func_name)
        print(resp)

def get_responses():
    dirName = os.path.join(os.getcwd(),'function','test_reqs')
    fileNames = [f.split('.')[0] for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]
    threads = []
    start = time.time()
    for f in fileNames:
        t = GetUrlThread(f)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Elapsed time: %s" % (time.time()-start))
# `run_function` receives `params` as a dict
# Return something which is serializable using `json.dumps()`



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
    request = Request(base_url + func_name,data=d,headers=HEADERS,)
    r = {"code": "none", "reason": "something went wrong"}
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
    return r
def interpret_status_code(code):
    if re.search("^2([0-9]+){2}", code):
        return "function was successful"
    return "request failed!"

def get_function_info(name):
    test_req_file = get_test_req(name)
    json_content  = json.dumps(test_req_file)
    start_time = time.time()
    return send_request(name,d=json_content.encode())
    # info = {"execution_time":(time.time() - start_time), "status": interpret_status_code(str(response.getcode()))}
    # return json.dumps(info)  
def run_function(params: dict):

    preprocess(params)
    
    if check_if_exists('func_name', params):
        if params["func_name"] == "all":
            get_responses()
            return
            # dirName = os.path.join(os.getcwd(),'function','test_reqs')
            # fileNames = [f.split('.')[0] for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]
            # result = []
            # for f in fileNames:
            #     print('executing test for {0}'.format(f))
            #     get_function_info(f)
            # return json.dumps(result)
        return get_function_info(params['func_name'])
