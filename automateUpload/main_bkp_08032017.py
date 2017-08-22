#!/usr/bin/ python

import os
import csv
import requests
import sys
import json
import APIMethod as APIFile

# Function helps in uploading files to DGC
def dgcUpload(jenkinsTargetFolderPath, deltaListFile):
    # Open the file path
    os.chdir(jenkinsTargetFolderPath)

    # Upload file to temporary location
    # Define file endpoint and payload
    fileEndpoint = 'file'
    filePayload = {'file': open(deltaListFile, 'rb')}

    # Make API call to upload the file to temporary location
    tempTryLogin = APIFile.API.postFileCall(fileEndpoint, filePayload)
    tempTryLoginJSON = tempTryLogin['data']

    # Fetch unique file identifier of the file
    fileid = tempTryLoginJSON['file'][0]

    # Upload file to DGC
    # Define workflow endpoint and payload
    workflowEndpoint = "workflow"
    workflowPayload = {'file': fileid, 'fileName': deltaListFile}

    # Make API call to upload the workflow to DGC from temporary location
    tryLogin = APIFile.API.postDataCall(workflowEndpoint , workflowPayload)

    return tryLogin['statusCode']

def findWorkflow(processName):
    # Define endpoint and payload
    endpoint = "workflow/find"
    payload = {'name': processName}

    # Call getCall from APIMethod to fetch the GET Response
    tryLogin = APIFile.API.getCall(endpoint, payload)

    # Convert GET Response to JSON
    tryLoginJSON = tryLogin['data']

    # Fetch 'workflowDefinitionReference' section from JSON string
    jsonString = tryLoginJSON['workflowDefinitionReference']

    # Find the length of the JSON string
    jsonLength = len(tryLoginJSON['workflowDefinitionReference'])

    # Loop through the JSON string to find whether the requested process exists in DGC
    for i in range(0, jsonLength):
        if jsonString[i]['signifier'] == processName:
            return jsonString[i]['resourceId']

    return 'Workflow Not Found'

def workflowPerformPostDataCall(endpoint, payload):
    # Kickoff the workflow using the endpoint and payload
    trylogin = APIFile.API.postDataCall(endpoint, payload)
    return trylogin['statusCode']

def workflowPerformPostSessionDataCall(endpoint, payload):
    # Kickoff the workflow using the endpoint and payload
    trylogin = APIFile.API.postSessionDataCall(endpoint , payload)
    return trylogin['statusCode']

# Main function
if __name__ == '__main__':

    # Find the Parameter File Name
    paramFileName = sys.argv[1]

    # Open the parameter file of the business process
    os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r') as jsonFile:
        paramFileData = json.load(jsonFile)

    # Loop through the values in parameter file to fetch parameters
    for key in paramFileData.keys():

        if key == 'JenkinsTargetFolder':
            jenkinsTargetFolderPath = paramFileData[key]

        if key == 'DeltaListPath':
            deltaListPath = paramFileData[key]

        if key == 'DeltaListFile':
            deltaListFile = paramFileData[key]

        if key == 'ProcessName':
            processName = paramFileData[key]

        if key == 'StatusCodeInDGC':
            statusCodeInDGC = paramFileData[key]

        if key == 'AppliesTo':
            appliesTo = paramFileData[key]

        if key == 'ConfigurationVariables':
            configurationVariable = paramFileData[key]

    # Change to the folder where the files are present
    os.chdir(deltaListPath)

    # Open deltalistfile to check for the changed code files
    deltaListData = open(deltaListFile, 'r')
    deltaListDataRow = csv.reader(deltaListData)

    # Upload each bpmn file to DGC
    for line in deltaListDataRow:
        if line[0].endswith('.bpmn'):

            # Upload the workflow to dgc
            uploadResponse = dgcUpload(jenkinsTargetFolderPath, line[0])

            if uploadResponse != '1':
                print('Error while uploading the workflow. Please check logs.')
                break
            elif uploadResponse == '1':
                print('File uploaded to DGC successfully.')

            # Find the ResourceId of the workflow
            resourceId = findWorkflow(processName)

            # Kickoff the workflow
            if resourceId != 'Workflow Not Found':
                # Kickoff workflow using the processId
                kickOffEndpoint = "term/" + resourceId + "/status"
                kickOffPayload = {'rid': resourceId, 'status': statusCodeInDGC}
                kickOffResponse = workflowPerformPostDataCall(kickOffEndpoint, kickOffPayload)

                if kickOffResponse != '1':
                    print('Error while kicking off the workflow. Please check logs.')
                    break
                elif kickOffResponse == '1':
                    print('Workflow kicked off successfully.')

                # Assign the 'Applies To' Attribute
                # Fetch the itemResourceType from the itemResourceType File
                itemResourceTypeFile = 'referenceData.json'

                # Open the itemResourceType file and find the itemResourceTypeCode
                os.chdir("K:\Git Code\Python\ParameterFiles")
                with open(itemResourceTypeFile) as jsonfile:
                    itemResourceType = json.load(jsonfile)
                    itemResourceTypeCode = itemResourceType['itemResourceType'][appliesTo]

                # Define endpoint and payload
                appliesToEndpoint = "workflow/" + resourceId + "/itemResourceType"
                appliesToPayload = {'itemResourceType': itemResourceTypeCode}
                appliesToResponse = workflowPerformPostDataCall(appliesToEndpoint, appliesToPayload)

                if appliesToResponse != '1':
                    print('Error while changing appliesTo attribute of the workflow. Please check logs.')
                    break
                elif appliesToResponse == '1':
                    print('Workflow appliesTo attributed changed successfully.')

                # Assign configuration variables
                configurationVariableEndpoint = "workflow/" + resourceId + "/configurationVariables/"
                configurationVariablePayload = paramFileData['ConfigurationVariables']
                configurationVariableResponse = workflowPerformPostSessionDataCall(configurationVariableEndpoint, configurationVariablePayload)

                if configurationVariableResponse != '1':
                    print('Error while changing configuration variables of the workflow. Please check logs.')
                    break
                elif configurationVariableResponse == '1':
                    print('Workflow configuration variables set successfully.')

                # Start event variables
                if 'startEvent' in paramFileData != '':
                    #Assign start event with variables defined
                    startEventEndpoint = "/workflow/" + resourceId + "/startEvent"
                    startEventPayload = {'eventTypes': paramFileData['startEvent']}
                    startEventResponse = workflowPerformPostSessionDataCall(startEventEndpoint, startEventPayload)

                    if startEventResponse != '1':
                        print('Error while changing Start Event variable of the workflow. Please check logs.')
                        break
                    elif startEventResponse == '1':
                        print('Workflow Start Event variable set successfully.')

                else:
                    print('FYI - No Start Event variables configured.')
            else:
                print('Workflow not found in DGC')