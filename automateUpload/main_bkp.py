#!/usr/bin/ python

import os
import csv
import requests
import sys
import json
import APIMethod as API


# Function helps in uploading files to DGC
def dgcupload(baseurl, restversion, user, passw, jenkinstargetfolderpath, deltalistfile):
    # Open the file path
    os.chdir(jenkinstargetfolderpath)

    # Upload file to temporary location
    tempurl = baseurl + restversion + '/file'
    filepayload = {'file': open(deltalistfile, 'rb')}
    temptrylogin = requests.post(tempurl, auth=(user, passw), files=filepayload)
    temptryloginjson = temptrylogin.json()

    # Generate unique file identifier
    fileid = temptryloginjson['file'][0]
    print('FileId: ' + fileid)
    print('Delta File: ' + deltalistfile)
    payload = {'file': fileid, 'fileName': deltalistfile}

    url = baseurl + restversion + "/workflow"
    print(url)

    trylogin = requests.post(url, auth=(user, passw), data=payload)

    if trylogin.status_code != 201:
        print('Error in the process. Please check logs')
    elif trylogin.status_code == 201:
        print('File uploaded successfully')


def findworkflow(baseurl, restversion, user, passw, deltalistfilename, checkfilename):
    # Define endpoint and payload
    endpoint = "/workflow/find"
    payload = {'name': deltalistfilename}

    # Call getCall from APIMethod to fetch the GET Response
    trylogin = API.getCall(endpoint, payload)

    # Convert GET Response to JSON
    tryloginjson = trylogin.json()

    # Fetch 'workflowDefinitionReference' section from JSON string
    jsonstring = tryloginjson['workflowDefinitionReference']

    # Find the length of the JSON string
    jsonlength = len(tryloginjson['workflowDefinitionReference'])

    # Loop through the JSON string to find whether the requested process exists in DGC
    for i in range(0, jsonlength):
        if jsonstring[i]['signifier'] == checkfilename:
            return jsonstring[i]['resourceId']

    return 'Workflow Not Found'


def workflowkickoff(baseurl, restversion, user, passw, resourceId):
    payload = {'rid': resourceId, 'status': '00000000-0000-0000-0000-000000005051'}
    url = baseurl + restversion + "/term/" + resourceId + "/status"
    print('kickoff :' + url)

    trylogin = requests.post(url, auth=(user, passw), data=payload)

    print(trylogin.content)
    print(trylogin.status_code)
    if trylogin.status_code != 200:
        print('Error in the process. Please check logs')
    elif trylogin.status_code == 200:
        print('Workflow kicked off successfully')


# Main function
if __name__ == '__main__':

    # Find the Parameter File Name
    paramFileName = sys.argv[1]

    # Open the parameter file
    os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r') as jsonfile:
        paramfiledata = json.load(jsonfile)

    print(paramfiledata['URL'])

    baseurl = paramfiledata['URL']
    user = paramfiledata['User']
    passw = paramfiledata['Pass']
    restversion = paramfiledata['RestVersion']
    jenkinstargetfolderpath = paramfiledata['JenkinsTargetFolder']
    deltalistpath = paramfiledata['DeltaListPath']
    deltalistfile = paramfiledata['DeltaListFile']

    # Change to the folder where the files are present
    os.chdir(deltalistpath)
    deltalistdata = open(deltalistfile, 'r')
    deltalistdatarow = csv.reader(deltalistdata)

    for line in deltalistdatarow:
        if line[0].endswith('.bpmn'):

            if line[0] == 'New Process - Approve Code Value.bpmn':
                deltalistfilename = 'Code Value Approval Process'
            else:
                deltalistfilename = line[0]

            # Upload the workflow to dgc
            dgcupload(baseurl, restversion, user, passw, jenkinstargetfolderpath, line[0])

            # Find the ResourceId of the workflow
            workflowexists = findworkflow(baseurl, restversion, user, passw, deltalistfilename,
                                          'Code Value Approval Process')

            # Kickoff the workflow
            if workflowexists != 'Workflow Not Found':
                workflowkickoff(baseurl, restversion, user, passw, workflowexists)

            # Assign the 'Applies To' Attribute
            if paramfiledata['AppliesTo'] != '':
                workflowa
