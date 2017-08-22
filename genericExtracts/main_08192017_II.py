#!/usr/bin/ python

import os
import sys
import yaml
import time
import APIMethod as APIFile
import csv
import math
import smtplib
import shutil
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate

def getDataCall(endpoint, payload):
    # Kickoff the workflow using the endpoint and payload
    trylogin = APIFile.API.getCall(endpoint, payload)

    return trylogin

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

def convertEpochTime(inputTime):

    mathTargetTime = math.ceil(int(inputTime) / 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))

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

                # targetTime = int(dataToBeFiltered[i][lookupKey])
                # mathTargetTime = math.ceil(targetTime / 1000)
                # dateTargetTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))
                dateTargetTime = convertEpochTime(dataToBeFiltered[i][lookupKey])
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


    return newMap

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

def fetchPossibleRelationsAndAttributes(resourceId):
    possibleRandAEndpoint = 'concept_type/' + resourceId + '/possible_attribute_relation_types'
    possibleRandAPayload = ''
    possibleRandAResponse = getDataCall(possibleRandAEndpoint, possibleRandAPayload)
    if possibleRandAResponse['statusCode'] == '1':
        return possibleRandAResponse['data']
    else:
        return 'No Data Found'

def fetchRelations(resourceId):
    relationsResponseList = []

    sourceError = 'true'
    targetError = 'true'

    sourceRelationsEndpoint = 'concept_type/' + resourceId + '/source_relations'
    sourceRelationsPayload = ''
    sourceRelationsResponse = getDataCall(sourceRelationsEndpoint, sourceRelationsPayload)
    if sourceRelationsResponse['statusCode'] == '1':
        relationsResponseList.append(sourceRelationsResponse['data'])
    else:
        sourceError = 'No Data Found'

    targetRelationsEndpoint = 'concept_type/' + resourceId + '/target_relations'
    targetRelationsPayload = ''
    targetRelationsResponse = getDataCall(targetRelationsEndpoint, targetRelationsPayload)
    if targetRelationsResponse['statusCode'] == '1':
        relationsResponseList.append(targetRelationsResponse['data'])
    else:
        targetError = 'No Data Found'

    if sourceError == 'true' and targetError == 'true':
        return relationsResponseList
    else:
        return 'No Data Found'

def fetchComplexRelations(resourceId):
    complexRelationDefinitionEndpoint = 'complex_relation/'
    complexRelationDefinitionPayload = {'term': resourceId}
    complexRelationDefinitionResponse = getDataCall(complexRelationDefinitionEndpoint, complexRelationDefinitionPayload)

    if complexRelationDefinitionResponse['statusCode'] == '1':
        complexRelationDefinitionData = complexRelationDefinitionResponse['data']
        if len(complexRelationDefinitionData['termReference']) == 0:
            return 'No Relations Found'
        else:
            complexRelationRelationsEndpoint = 'complex_relation/' + complexRelationDefinitionData['termReference'][0]['resourceId'] + '/relations'
            complexRelationRelationsPayload = ''
            complexRelationRelationsResponse = getDataCall(complexRelationRelationsEndpoint, complexRelationRelationsPayload)
            if complexRelationRelationsResponse['statusCode'] == '1':
                return complexRelationRelationsResponse['data']
            else:
                return 'No Data Found'

def fetchComplexRelationsAttributes(resourceId):
    complexRelationDefinitionEndpoint = 'complex_relation/'
    complexRelationDefinitionPayload = {'term': resourceId}
    complexRelationDefinitionResponse = getDataCall(complexRelationDefinitionEndpoint,
                                                    complexRelationDefinitionPayload)

    if complexRelationDefinitionResponse['statusCode'] == '1':
        complexRelationDefinitionData = complexRelationDefinitionResponse['data']
        if len(complexRelationDefinitionData['termReference']) == 0:
            return 'No Attributes Found'
        else:
            complexRelationAttributesEndpoint = 'complex_relation/' + complexRelationDefinitionData['termReference'][0]['resourceId']
            complexRelationAttributesPayload = ''
            complexRelationAttributesResponse = getDataCall(complexRelationAttributesEndpoint,complexRelationAttributesPayload)
            if complexRelationAttributesResponse['statusCode'] == '1':
                return complexRelationAttributesResponse['data']
            else:
                return 'No Data Found'

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
                if itemkey != 'outputFileName' and itemkey != 'email':
                    tempTargetData = fetchDataSet(itemkey, eachMap[itemkey])
                    targetData = filterTargetData(eachMap, tempTargetData)
                    targetDataRelationsMap = {}
                    targetDataAttributesMap = {}
                    targetDataComplexRelationsMap = {}
                    # Find the Relations, Attributes and Complex Relations of the asset
                    for i in range(0, len(targetData)):
                        # Find the possible Relations and Attributes of the asset

                        possibleRelationsAndAttributesResponse = fetchPossibleRelationsAndAttributes(targetData[i]['resourceId'])
                        possibleRelationAttributesList = []
                        possibleRelationRelationsList = []

                        if possibleRelationsAndAttributesResponse != 'No Data Found':

                            possibleRelationsAndAttributesList = possibleRelationsAndAttributesResponse['representationReference']

                            for k in range(0,len(possibleRelationsAndAttributesList)):

                                if 'descriptionReference' in possibleRelationsAndAttributesList[k].keys():
                                    possibleRelationAttributesList.append(possibleRelationsAndAttributesList[k]['signifier'])

                                tempMap = {}

                                if 'role' in possibleRelationsAndAttributesList[k].keys():

                                    tempMap['role'] = possibleRelationsAndAttributesList[k]['role']
                                    tempMap['coRole'] = possibleRelationsAndAttributesList[k]['coRole']
                                    if tempMap not in possibleRelationRelationsList:
                                        possibleRelationRelationsList.append(tempMap)

                        print()
                        # Find the Relations
                        targetDataRelationsMap = {}
                        targetDataRelationsMap['signifier'] = targetData[i]['signifier']
                        relationsResponse = fetchRelations(targetData[i]['resourceId'])

                        if relationsResponse != 'No Data Found':

                            for relationsResponseList in relationsResponse:

                                relationsMap = relationsResponseList['relation']

                                for innerRelationsMap in relationsMap:

                                    for roleMap in possibleRelationRelationsList:

                                        if innerRelationsMap['typeReference']['role'] == roleMap['role']:
                                            targetDataRelationsMap['role'] = innerRelationsMap['sourceReference'] ['signifier']
                                            targetDataRelationsMap['coRole'] = innerRelationsMap['targetReference']['signifier']

                            #print(targetDataRelationsMap)

                        # Find the Complex Relations and Attributes
                        targetDataComplexRelationsMap['signifier'] = targetData[i]['signifier']
                        complexRelationsMap = fetchComplexRelations(targetData[i]['resourceId'])

                        if complexRelationsMap != 'No Data Found' and complexRelationsMap != 'No Relations Found':
                            relationValue = []

                            for j in range(0, len(complexRelationsMap['relationReference'])):
                                relationReferenceList = complexRelationsMap['relationReference'][j]
                                relationKey = relationReferenceList['typeReference']['role']
                                if relationKey in targetDataComplexRelationsMap.keys():
                                    relationValue = targetDataComplexRelationsMap[relationKey]
                                relationValue.append(relationReferenceList['targetReference']['signifier'])
                                targetDataComplexRelationsMap[relationKey] = relationValue
                                relationValue = []

                        complexRelationsAttributesMap = fetchComplexRelationsAttributes(targetData[i]['resourceId'])

                        if complexRelationsAttributesMap != 'No Attributes Found':
                            attributeValue = []
                            for j in range(0, len(complexRelationsAttributesMap['attributeReferences']['attributeReference'])):
                                attributesReferenceList = complexRelationsAttributesMap['attributeReferences']['attributeReference'][j]
                                attributeKey = attributesReferenceList['labelReference']['signifier']
                                if attributeKey in targetDataComplexRelationsMap.keys():
                                    attributeValue = targetDataComplexRelationsMap[attributeKey]
                                attributeValue.append(attributesReferenceList['value'])
                                targetDataComplexRelationsMap[attributeKey] = attributeValue
                                attributeValue = []



                elif itemkey == 'outputFileName':
                    outputFileName = eachMap[itemkey]
                    targetFileName = 'K:/Git Code/Python/Output/'+eachMap[itemkey]+'.csv'
                    targetFile = open(targetFileName, 'w', newline='')
                    csvWriter = csv.writer(targetFile, delimiter=',')
                    csvWriter.writerow(['Community','Domain','Asset Type','Asset Name','Status', 'Articulation Score', 'Created On', 'Created By',  'Last Modified', 'Last Modified By'])

                    writeString = []
                    for i in range(0,len(targetData)):
                        # Community
                        if 'vocabularyReference' in targetData[i]:
                            if 'communityReference' in targetData[i]['vocabularyReference']:
                                if 'name' in targetData[i]['vocabularyReference']['communityReference']:
                                    writeString.append(targetData[i]['vocabularyReference']['communityReference']['name'])
                                else:
                                    writeString.append('Not Applicable')
                            else:
                                writeString.append('Not Applicable')
                        else:
                            writeString.append('Not Applicable')

                        # Domain
                        if 'vocabularyReference' in targetData[i]:
                            if 'name' in targetData[i]['vocabularyReference']:
                                writeString.append(targetData[i]['vocabularyReference']['name'])
                            else:
                                writeString.append('Not Applicable')
                        else:
                            writeString.append('Not Applicable')

                        # Asset Type
                        if 'conceptType' in targetData[i]:
                            if 'signifier' in targetData[i]['conceptType']:
                                writeString.append(targetData[i]['conceptType']['signifier'])
                            else:
                                writeString.append('Not Applicable')
                        else:
                            writeString.append('Not Applicable')

                        # Asset Name
                        if 'signifier' in targetData[i]:
                            writeString.append(targetData[i]['signifier'])
                        else:
                            writeString.append('Not Applicable')

                        # Status
                        if 'statusReference' in targetData[i]:
                            if 'signifier' in targetData[i]['statusReference']:
                                writeString.append(targetData[i]['statusReference']['signifier'])
                            else:
                                writeString.append('Not Applicable')
                        else:
                            writeString.append('Not Applicable')

                        writeString.append(targetData[i].get('articulation','Not Applicable'))  # Articulation Score
                        writeString.append(convertEpochTime(targetData[i].get('createdOn'))) # Created On
                        writeString.append(targetData[i]['createdBy']['firstName'] + targetData[i]['createdBy']['lastName']) # Created By
                        writeString.append(convertEpochTime(targetData[i].get('lastModified')))  # Last Modified
                        writeString.append(targetData[i]['lastModifiedBy']['firstName'] + targetData[i]['lastModifiedBy']['lastName']) # Last Modified By

                        csvWriter.writerow(writeString)
                        writeString = []


                    targetFileName = 'K:/Git Code/Python/Output/' + targetDataComplexRelationsMap['signifier'] + '_ComplexRelations.csv'
                    targetFile = open(targetFileName, 'w', newline='')
                    csvWriter = csv.writer(targetFile, delimiter=',')

                    targetFileHeader = []
                    for key in targetDataComplexRelationsMap.keys():
                        targetFileHeader.append(key)

                    csvWriter.writerow(targetFileHeader)

                    targetFileRow = []
                    for key in targetDataComplexRelationsMap.keys():
                        if isinstance(targetDataComplexRelationsMap[key], list):
                            writeString = ','.join(str(x) for x in targetDataComplexRelationsMap[key])
                        else:
                            writeString = targetDataComplexRelationsMap[key]
                        targetFileRow.append(writeString)
                        writeString = ''

                    csvWriter.writerow(targetFileRow)


                elif itemkey == 'email':

                    outputFilePath = "K:/Git Code/Python/Output/" + outputFileName + ".csv"
                    filePath = "K:/Git Code/Python/Output/data.txt"

                    if os.path.isfile(outputFilePath):

                        composedMessage = MIMEMultipart()
                        composedMessage['Subject'] = 'Requested Information'
                        composedMessage['To'] = eachMap[itemkey]
                        composedMessage['From'] = "srikrishna.bingi@gmail.com"

                        ctype, encoding = mimetypes.guess_type(outputFilePath)
                        if ctype is None or encoding is not None:
                            ctype = "application/octet-stream"

                        maintype, subtype = ctype.split("/", 1)

                        with open(outputFilePath, newline='') as fp:
                            msg = MIMEBase(maintype, _subtype=subtype)
                            msg.set_payload(fp.read())
                            encoders.encode_base64(msg)

                        msg.add_header("Content-Disposition", "attachment", filename=outputFileName)
                        composedMessage.attach(msg)

                        mailObject = smtplib.SMTP('smtp.gmail.com', 587)
                        mailObject.starttls()
                        mailObject.login('srikrishna.bingi@gmail.com','Sri13krishna')
                        #mailObject.sendmail("srikrishna.bingi@gmail.com","srikrishna.bingi@exusia.com",composedMessage.as_string())
                        print('Done sending Mail')

                        mailObject.close()