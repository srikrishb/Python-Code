#!/usr/bin/ python

import os
import sys
import yaml
import time
import APIMethod as APIFile
import csv
import math
import operator
import string

def getDataCall(endpoint, payload):
    # Kickoff the workflow using the endpoint and payload
    trylogin = APIFile.API.getCall(endpoint, payload)

    return trylogin

# def applyOperand(key, resultSet):
#     if key == 'Or':
#         # Apply filters on targetData
#         pass

def fetchDataSet(innerMapKey, innerMapValue):

    result = dict()
    if innerMapKey.find("lastModified") != -1:
        searchSignfier = ''
    elif innerMapKey == 'assetNameLike' or innerMapKey == 'assetNameEquals':
        searchSignfier = innerMapValue

    if innerMapKey == 'assetNameLike' or innerMapKey == 'assetNameEquals' or innerMapKey.find("lastModified") != -1:
            assetNameLikeEndpoint = 'term/find/full'
            assetNameLikePayload = {'excludeMeta': 'false', 'searchSignifier': searchSignfier}
            assetNameLikeResponse = getDataCall(assetNameLikeEndpoint, assetNameLikePayload)


            if assetNameLikeResponse['statusCode'] == '1':

                # with open('K:/Git Code/Python/Output/content.json') as rawJSONData:
                #     result = json.load(rawJSONData)
                #     for key in result.keys():
                #         print(key)

                result = assetNameLikeResponse['data']['term']

    return result

def filterTargetData(innerMap, dataToBeFiltered):
    filteredData = []

    for key in innerMap.keys():
        filterValue = innerMap[key]

        if str.upper(key).find("LASTMODIFIED") != -1 or str.upper(key).find("CREATED") != -1:
            if str.upper(key).find("LASTMODIFIED") != -1:
                lookupKey = 'lastModified'
            elif str.upper(key).find("CREATEDBEFORE") or key.find("CREATEDAFTER") or key.find("CREATEDBETWEEN") != -1:
                lookupKey = 'createdOn'

            i = 0
            for data in dataToBeFiltered:

                targetTime = int(dataToBeFiltered[i][lookupKey])
                mathTargetTime = math.ceil(targetTime / 1000)

                dateTargetTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))

                if str.upper(key).find("AFTER") !=-1:
                    if dateTargetTime > filterValue:
                        filteredData.append(data)
                elif str.upper(key).find("BEFORE") !=-1:
                    if dateTargetTime < filterValue:
                        filteredData.append(data)
                elif str.upper(key).find("BETWEEN") !=-1:

                    term1 = filterValue[0]
                    term2 = filterValue[1]
                    if dateTargetTime >= term1 and dateTargetTime <= term2:
                        filteredData.append(data)

                i += 1
        elif str.upper(key).find("ASSET") != -1:
            return dataToBeFiltered
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
                print('caught')
                pass
            else:
                if itemkey != 'outputFileName':
                    tempTargetData = fetchDataSet(itemkey, eachMap[itemkey])
                    targetData = filterTargetData(eachMap, tempTargetData)
                elif itemkey == 'outputFileName':
                    targetFileName = 'K:/Git Code/Python/Output/'+eachMap[itemkey]
                    targetFile = open(targetFileName, 'w', newline='')
                    csvWriter = csv.writer(targetFile, delimiter=',')
                    csvWriter.writerow(['Asset Name', 'Created By', 'Last Modified By', 'Last Modified'])

                    writeString = []

                    for i in range(0,len(targetData)):

                        writeString.append(targetData[i]['signifier'])
                        writeString.append(targetData[i]['createdBy']['firstName'] + targetData[i]['createdBy']['lastName'])
                        writeString.append(
                            targetData[i]['lastModifiedBy']['firstName'] + targetData[i]['lastModifiedBy']['lastName'])

                        targetTime = int(targetData[i]['lastModified'])
                        mathTargetTime = math.ceil(targetTime / 1000)
                        writeString.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime)))

                        csvWriter.writerow(writeString)


                        writeString = []