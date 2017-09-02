#!/usr/bin/ python

import os
import sys
import yaml
import time
import APIMethod as APIFile
import csv
import math


def getDataCall(endpoint, payload):
    # Kickoff the workflow using the endpoint and payload
    trylogin = APIFile.API.getCall(endpoint, payload)
    return trylogin

# def applyOperand(key, resultSet):
#     if key == 'Or':
#         # Apply filters on targetData
#         pass

def fetchDataSet(innerMap):

    for innerMapKey in innerMap.keys():

        if innerMapKey.find("lastModified"):
            searchSignfier = ''
        elif innerMapKey == 'assetNameLike' or innerMapKey == 'assetNameEquals':
            searchSignfier = eachMap[innerMapKey]

        if innerMapKey == 'assetNameLike' or innerMapKey == 'assetNameEquals' or innerMapKey.find("lastModified"):
                assetNameLikeEndpoint = 'term/find/full'
                assetNameLikePayload = {'excludeMeta': 'false', 'searchSignifier': searchSignfier}
                assetNameLikeResponse = getDataCall(assetNameLikeEndpoint, assetNameLikePayload)

                result = assetNameLikeResponse['data']['term']

    return result


def filterTargetData(innerMap, dataToBeFiltered):
    filteredData = {}
    for key in innerMap.keys():
        filterValue = innerMap[key]
        print(filterValue)
        if key == 'lastModifiedAfter':

            i = 0
            for data in dataToBeFiltered:

                targetTime = int(dataToBeFiltered[i]['lastModified'])
                mathTargetTime = math.ceil(targetTime / 1000)
                dateTargetTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))

                if dateTargetTime > filterValue:
                    #filteredData.update(data)
                    print(filteredData)
                i += 1


    return filteredData

# def createMap(innerMap):
#     totalLength = 0
#     notdictcount = 0
#     for key in innerMap.keys():
#         if isinstance(innerMap[key],dict):
#             if key == 'Or' or key == 'And':
#                 operand = key
#                 resultSet = fetchDataSet(innerMap[key])
#                 targetData = applyOperand(key, resultSet)
#             else:
#                 targetData = fetchDataSet(innerMap[key])
#                 count=0
#                 if innerMap[key] == 'outputFileName' and count == 1:
#
#                     targetFileName = 'K:/Git Code/Python/Output/' + eachMap[key]
#                     targetFile = open(targetFileName, 'w', newline='')
#                     csvWriter = csv.writer(targetFile, delimiter=',')
#
#                     csvWriter.writerow(['Asset Name', 'Created By', 'Last Modified By', 'Status'])
#
#                     writeString = []
#
#                     i = 0
#                     for data in targetData:
#                         targetTime = int(targetData[i]['lastModified'])
#                         mathTargetTime = math.ceil(targetTime / 1000)
#                         print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime)))
#
#                         writeString.append(targetData[i]['signifier'])
#                         writeString.append(targetData[i]['createdBy']['firstName'] + targetData[i]['createdBy']['lastName'])
#                         writeString.append(
#                             targetData[i]['lastModifiedBy']['firstName'] + targetData[i]['lastModifiedBy']['lastName'])
#                         writeString.append(targetData[i]['statusReference']['signifier'])
#                         csvWriter.writerow(writeString)
#
#                         writeString = []
#                         i += 1
#
#                         targetFile.close()
#                         count -= 1
#
#         else:
#             targetData = createFile(innerMap[key])
#
#     return notdictcount

# Main function
if __name__ == '__main__':

    # Find the Parameter File Name
    paramFileName = sys.argv[1]

    # Open the parameter file of the business process
    os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r') as yamlFile:
        paramFileData = yaml.load(yamlFile)

    for eachKey in paramFileData.keys():
        eachMap = paramFileData[eachKey]

        for itemkey in eachMap.keys():

            if isinstance(eachMap[itemkey], dict):
                #createMap(eachMap[itemkey])
                pass
            else:
                if itemkey != 'outputFileName':
                    tempTargetData = fetchDataSet(eachMap)
                    targetData = filterTargetData(eachMap, tempTargetData)
                elif itemkey == 'outputFileName':
                    targetFileName = 'K:/Git Code/Python/Output/'+eachMap[itemkey]
                    targetFile = open(targetFileName, 'w', newline='')
                    csvWriter = csv.writer(targetFile, delimiter=',')
                    csvWriter.writerow(['Asset Name', 'Created By', 'Last Modified By', 'Last Modified'])

                    i = 0
                    writeString = []
                    #print(targetData)
                    #for data in targetData:
                        #print(targetData[i])
                        # writeString.append(targetData[i]['signifier'])
                        # writeString.append(
                        #     targetData[i]['createdBy']['firstName'] + targetData[i]['createdBy']['lastName'])
                        # writeString.append(
                        #     targetData[i]['lastModifiedBy']['firstName'] + targetData[i]['lastModifiedBy']['lastName'])
                        #
                        # targetTime = int(targetData[i]['lastModified'])
                        # mathTargetTime = math.ceil(targetTime / 1000)
                        # writeString.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime)))
                        #
                        # csvWriter.writerow(writeString)
                        #
                        # i += 1
                        #
                        # writeString = []