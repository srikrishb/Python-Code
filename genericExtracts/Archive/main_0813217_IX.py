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
    if str.upper(innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find("CREATED") != -1:
        searchSignfier = ''
    elif str.upper(innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS':
        searchSignfier = innerMapValue

    if str.upper(innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS' or str.upper(innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find("CREATED") != -1:
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

def listUnion(refList , dataList):

    newList = []
    newMap = refList

    for item in refList:
        newList.append(item['resourceId'])

    for items2 in dataList:
        if items2['resourceId'] not in newList:
            newMap.append(items2)

    print(newMap)
    return newList

def createMap(innerMap):
    tempMap = {}
    targetData = {}

    for key in innerMap.keys():
        # if isinstance(innerMap[key], dict) == 'false':

        if key == 'Or' or key == 'And':
            criteriaMap = innerMap[key]
            i = 0
            for criteriaKey in criteriaMap.keys():
                tempMap[criteriaKey] = criteriaMap[criteriaKey]

                if i == 0:
                    i += 1
                    tempTargetData = fetchDataSet(criteriaKey, criteriaMap[criteriaKey])
                    preTargetData = filterTargetData(tempMap, tempTargetData)


                else:

                    if key == 'And':
                        targetData = filterTargetData(tempMap, preTargetData)
                        preTargetData = targetData

                    if key == 'Or':
                        tempTargetData = fetchDataSet(criteriaKey, criteriaMap[criteriaKey])
                        newTargetData = filterTargetData(tempMap, tempTargetData)

                        targetData = listUnion(newTargetData, preTargetData)


                tempMap = {}
            # targetFileName = 'request12.csv'
            # targetFile = open(targetFileName, 'w', newline='')
            # csvWriter = csv.writer(targetFile, delimiter=',')
            # csvWriter.writerow(['Asset Name', 'Created By', 'Last Modified By', 'Last Modified'])
            #
            # writeString = []
            #
            # for i in range(0, len(targetData)):
            #     writeString.append(targetData[i]['signifier'])
            #     writeString.append(
            #         targetData[i]['createdBy']['firstName'] + targetData[i]['createdBy']['lastName'])
            #     writeString.append(
            #         targetData[i]['lastModifiedBy']['firstName'] + targetData[i]['lastModifiedBy'][
            #             'lastName'])
            #
            #     targetTime = int(targetData[i]['lastModified'])
            #     mathTargetTime = math.ceil(targetTime / 1000)
            #     writeString.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime)))
            #
            #     csvWriter.writerow(writeString)
            #     writeString = []





        # else:
        #     targetData = createFile(innerMap[key])

    return targetData

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
                targetData = createMap(eachMap)
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

                    print(targetData[0])
                    print(targetData[1])
                    # for i in range(0,len(targetData)):
                    #
                    #     print(targetData[i])
                    #     # writeString.append(targetData[i]['signifier'])
                        # writeString.append(targetData[i]['createdBy']['firstName'] + targetData[i]['createdBy']['lastName'])
                        # writeString.append(
                        #     targetData[i]['lastModifiedBy']['firstName'] + targetData[i]['lastModifiedBy']['lastName'])
                        #
                        # targetTime = int(targetData[i]['lastModified'])
                        # mathTargetTime = math.ceil(targetTime / 1000)
                        # writeString.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime)))
                        #
                        # csvWriter.writerow(writeString)
                        #
                        #
                        # writeString = []