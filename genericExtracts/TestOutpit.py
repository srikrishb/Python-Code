import APIMethod as APIFile
import json
import os
import sys
import time

def getDataCall(endpoint, payload):
    # Kickoff the workflow using the endpoint and payload
    trylogin = APIFile.API.getCall(endpoint, payload)
    return trylogin

def postSessionDataCall(endpoint, payload):
    # Kickoff the workflow using the endpoint and payload
    trylogin = APIFile.API.postSessionDataCall(endpoint, payload)
    return trylogin

if __name__ == '__main__':

    paramFileName = sys.argv[1]

    os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r', encoding='utf8') as jsonFile:
        paramFileData = json.load(jsonFile)

    endpoint = 'output/excel'
    payload = {'file':'DataFile', 'tableViewConfig': json.dumps(paramFileData)}

    response = postSessionDataCall(endpoint, payload)

    jobState = 'RUNNING'
    while jobState == 'RUNNING':
        jobEndpoint = "job/" + response['data']
        jobResponse = getDataCall(jobEndpoint, '')
        jobState = jobResponse['data']['state']

    jobMessage = json.loads(jobResponse['data']['message'])
    print(jobMessage)
    print(jobMessage['id'])