import os
import sys
import yaml
import re
from AttributeFilter import AttributeFilter
from RelationFilter import RelationFilter
from ComplexRelationFilter import ComplexRelationFilter
from Asset import Asset
from CreateMap import CreateMap
from CreateDataFile import CreateDataFile

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.replace(u'\xa0', u' ')
  return cleantext

if __name__ == '__main__':

    # Find the Parameter File Name
    paramFileName = sys.argv[1]

    # Open the parameter file of the business process
    os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r', encoding='utf8') as yamlFile:
        paramFileData = yaml.load(yamlFile)

    outputFilter = ''
    outputFileName = ''
    for eachKey in paramFileData.keys():
        fileNameList = []
        finalMap = {}
        finalResultList = []
        eachMap = paramFileData[eachKey]
        for itemkey in eachMap.keys():
            if itemkey == 'conditions':
                outputFilter = eachMap[itemkey].keys()
                if 'relationFilter' not in outputFilter and 'complexRelationFilter' not in outputFilter and 'attributeFilter' not in outputFilter:
                    if isinstance(eachMap[itemkey], dict):
                        targetData = CreateMap.generateMap(eachMap[itemkey])
                elif 'attributeFilter' in outputFilter:
                    tempMap = {}
                    for valuesMap in eachMap[itemkey].values():
                        for innerKey in valuesMap:
                            tempMap[innerKey] = valuesMap[innerKey]
                            if innerKey == 'attributeTypeEquals':
                                assetFilterObj = AttributeFilter(tempMap)
                                attributeKey = valuesMap[innerKey]
                                tempTargetData = Asset.fetchDataSet(innerKey, '')
                                preTargetData = assetFilterObj.filterAttributeDataSet(tempTargetData)
                                targetData = preTargetData
                                tempMap = {}
                            elif innerKey == 'attributeValueEquals':
                                filterAssetTypes = AttributeFilter(tempMap)
                                targetData = filterAssetTypes.filterTargetDataSet(attributeKey, preTargetData)
                elif 'complexRelationFilter' in outputFilter:
                    tempMap = {}
                    for valuesMap in eachMap[itemkey].values():
                        for innerKey in valuesMap:
                            tempMap[innerKey] = valuesMap[innerKey]
                            if innerKey == 'complexRelationName':
                                complexRelationFilterObj = ComplexRelationFilter(tempMap)
                                tempTargetData = Asset.fetchDataSet(innerKey,'')
                                preTargetData = complexRelationFilterObj.filterComplexRelationDataSet(tempTargetData)
                                targetData = preTargetData
                                tempMap = {}
                            elif innerKey == 'AssetType':
                                filterAssetTypes = ComplexRelationFilter(tempMap)
                                targetData = filterAssetTypes.filterTargetDataSet(preTargetData)
                elif 'relationFilter' in outputFilter:
                    tempMap = {}
                    for valuesMap in eachMap[itemkey].values():
                        for innerKey in valuesMap:
                            tempMap[innerKey] = valuesMap[innerKey]
                            if innerKey == 'RelationTypeIn':
                                relationFilterObj = RelationFilter(tempMap)
                                tempTargetData = Asset.fetchDataSet(innerKey, '')
                                preTargetData = relationFilterObj.filterRelationDataSet(tempTargetData)
                                targetData = preTargetData
                                tempMap = {}
                            elif innerKey == 'AssetType':
                                filterAssetTypes = RelationFilter(tempMap)
                                targetData = filterAssetTypes.filterTargetDataSet(preTargetData)
            elif itemkey == 'outputResult':
                if outputFilter != 'relationPath':
                    targetDataMap = {}
                    outputResultParameters = eachMap[itemkey]
                    for i in range(0, len(targetData)):
                        targetDataRelationsMap = {}
                        targetDataAttributesMap = {}
                        targetDataComplexRelationsMap = {}
                        targetDataComplexRelationsRelationsMap = {}
                        targetDataComplexRelationsAttributesMap = {}
                        targetDataMap = {}
                        attributeValue = []
                        tempList = []
                        assetName = targetData[i]['signifier']
                        assetObj = Asset(targetData[i]['resourceId'])
                        for outputParameter in outputResultParameters.keys():
                            outputParameterList = outputResultParameters[outputParameter]
                            # targetDataMap['Status'] = targetData[i]['statusReference']['signifier']
                            if outputParameter == 'Asset Details':
                                for detailType in outputParameterList:
                                    targetDataMap[detailType] = assetObj.fetchAssetAssetDetails(detailType, targetData[i])

                            # If needed, find the Relations, Attributes and Complex Relations of the asset
                            if outputParameter in ('Attributes', 'Relations'):
                                # Find the possible Relations and Attributes of the asset
                                #possibleRelationsAndAttributesResponse = fetchPossibleRelationsAndAttributes(targetData[i]['resourceId'])
                                possibleRelationsAndAttributesResponse = assetObj.fetchPossibleRelationsTypesAndAttributesTypes()
                                possibleAttributeTypesList = []
                                possibleRelationTypesList = []

                                if possibleRelationsAndAttributesResponse != 'No Data Found':
                                    possibleRelationsAndAttributesList = possibleRelationsAndAttributesResponse['representationReference']
                                    for k in range(0, len(possibleRelationsAndAttributesList)):
                                        if 'descriptionReference' in possibleRelationsAndAttributesList[k].keys():
                                            possibleAttributeTypesList.append(possibleRelationsAndAttributesList[k]['signifier'])
                                        tempMap = {}
                                        if 'role' in possibleRelationsAndAttributesList[k].keys():
                                            tempMap['role'] = possibleRelationsAndAttributesList[k]['role']
                                            tempMap['coRole'] = possibleRelationsAndAttributesList[k]['coRole']
                                            if tempMap not in possibleRelationTypesList:
                                                possibleRelationTypesList.append(tempMap)

                                # Find the Relations
                                if outputParameter == 'Relations':
                                    if outputParameterList == 'All':
                                        targetDataRelationsMap = {}
                                        relationsResponse = assetObj.fetchRelations()
                                        if relationsResponse != 'No Data Found':
                                            # Add all the relation types that have a value
                                            for relationResponseMap in relationsResponse:
                                                existingRoleKeyValue = []
                                                existingCoRoleKeyValue = []

                                                for innerRelationsMap in relationResponseMap['relation']:

                                                    if 'vocabularyReference' in innerRelationsMap['typeReference']['headTerm']:
                                                        relationType = innerRelationsMap['typeReference']['headTerm']['vocabularyReference']['name']

                                                    if relationType != 'Complex Relation Types':

                                                        targetDataRelationsRolekey = innerRelationsMap['typeReference']['role']
                                                        targetDataRelationsCoRolekey = innerRelationsMap['typeReference']['coRole']

                                                        if targetDataRelationsRolekey in targetDataRelationsMap.keys():
                                                            #print('1', targetDataRelationsRolekey,targetDataRelationsMap[targetDataRelationsRolekey])
                                                            existingRoleKeyValue = targetDataRelationsMap[targetDataRelationsRolekey]

                                                        if targetDataRelationsCoRolekey in targetDataRelationsMap.keys():
                                                            #print('2' , targetDataRelationsCoRolekey,targetDataRelationsMap[targetDataRelationsCoRolekey])
                                                            existingCoRoleKeyValue = targetDataRelationsMap[targetDataRelationsCoRolekey]

                                                        if innerRelationsMap['targetReference']['signifier'] == assetName:
                                                            existingRoleKeyValue = assetName
                                                            #print('3', existingRoleKeyValue)
                                                        else:
                                                            existingRoleKeyValue.append(innerRelationsMap['targetReference']['signifier'])
                                                            #print('4', existingRoleKeyValue)

                                                        if innerRelationsMap['sourceReference']['signifier'] == assetName:
                                                            existingCoRoleKeyValue = assetName
                                                            #print('5', existingCoRoleKeyValue, innerRelationsMap['sourceReference']['signifier'], assetName)
                                                        else:
                                                            #print('6', existingCoRoleKeyValue, assetName, innerRelationsMap['sourceReference']['signifier'])
                                                            existingCoRoleKeyValue.append(innerRelationsMap['sourceReference']['signifier'])

                                                        # Creating Temp Keys for map to avoid situations where coRole and Role get reused for both South and Target relations
                                                        tempRolekey = innerRelationsMap['typeReference']['resourceId']+'>'+innerRelationsMap['typeReference']['role']
                                                        targetDataRelationsMap[tempRolekey] = existingRoleKeyValue
                                                        tempCoRoleKey = innerRelationsMap['typeReference']['resourceId']+'>'+innerRelationsMap['typeReference']['coRole']
                                                        targetDataRelationsMap[tempCoRoleKey] = existingCoRoleKeyValue

                                            # Add all the relation types that don't have a value
                                            for possibleRelationType in possibleRelationTypesList:
                                                for roleMap in possibleRelationType:
                                                    if possibleRelationType[roleMap] not in targetDataRelationsMap.keys():
                                                        targetDataRelationsMap[possibleRelationType[roleMap]] = ''

                                # Find the Attributes
                                if outputParameter == 'Attributes' and len(possibleAttributeTypesList) > 0:

                                    targetDataAttributesMap = {}
                                    attributesResponse = assetObj.fetchAttributes()
                                    attributesResponseList = attributesResponse['attributeReference']

                                    if outputParameterList == 'All':
                                        # Add all the attribute types that have a value
                                        for listIndex in range(0, len(attributesResponseList)):
                                            attributeResponseMap = attributesResponseList[listIndex]
                                            existingKeyValue = []
                                            # key = attributeResponseMap['resourceId'] + ' -> ' + attributeResponseMap['labelReference']['signifier']
                                            key = attributeResponseMap['labelReference']['signifier']
                                            cleanedKeyValue = cleanhtml(attributeResponseMap['value'])
                                            if key in targetDataAttributesMap.keys():
                                                existingKeyValue = targetDataAttributesMap[key]
                                            existingKeyValue.append(cleanedKeyValue)
                                            targetDataAttributesMap[key] = existingKeyValue
                                        # Add all the attribute types that don't have a value
                                        for possibleAttribute in possibleAttributeTypesList:
                                            if possibleAttribute not in targetDataAttributesMap.keys():
                                                targetDataAttributesMap[possibleAttribute] = ''
                                    else:
                                        # Add all the attribute types that have a value
                                        for listIndex in range(0, len(attributesResponseList)):
                                            attributeResponseMap = attributesResponseList[listIndex]
                                            existingKeyValue = []
                                            # key = attributeResponseMap['resourceId'] + ' -> ' + attributeResponseMap['labelReference']['signifier']
                                            key = attributeResponseMap['labelReference']['signifier']
                                            if key in outputParameterList:
                                                cleanedKeyValue = cleanhtml(attributeResponseMap['value'])
                                                if key in targetDataAttributesMap.keys():
                                                    existingKeyValue = targetDataAttributesMap[key]
                                                existingKeyValue.append(cleanedKeyValue)
                                                targetDataAttributesMap[key] = existingKeyValue
                                        # Add all the attribute types that don't have a value
                                        for attributeType in outputParameterList:
                                            if attributeType not in targetDataAttributesMap.keys():
                                                targetDataAttributesMap[attributeType] = ''

                            if outputParameter == 'Complex Relations':
                                # Find the Complex Relations and Attributes
                                complexRelationsMapList = assetObj.fetchComplexRelations()
                                if complexRelationsMapList not in ('No Relations Found', 'No Data Found'):
                                    relationValue = []
                                    tempMap = {}
                                    for complexRelationsMap in complexRelationsMapList:
                                        for j in range(0, len(complexRelationsMap['relationReference'])):
                                            relationReferenceList = complexRelationsMap['relationReference'][j]
                                            # Check if there is any existing entry for the same signifier
                                            if relationReferenceList['typeReference']['headTerm']['signifier'] in targetDataComplexRelationsRelationsMap.keys():
                                                tempMap = targetDataComplexRelationsRelationsMap[relationReferenceList['typeReference']['headTerm']['signifier']]
                                            else:
                                                tempMap = {}
                                            relationKey = relationReferenceList['typeReference']['role']
                                            if relationKey in tempMap.keys():
                                                relationValue = tempMap[relationKey]
                                            relationValue.append(relationReferenceList['targetReference']['signifier'])
                                            tempMap[relationKey] = relationValue
                                            targetDataComplexRelationsRelationsMap[relationReferenceList['typeReference']['headTerm']['signifier']]= tempMap
                                            relationValue = []
                                            targetDataComplexRelationsMap['Relation'] = targetDataComplexRelationsRelationsMap

                                complexRelationsAttributesMapList = assetObj.fetchComplexRelationsAttributes()
                                if complexRelationsAttributesMapList != 'No Attributes Found':

                                    for complexRelationsAttributesMap in complexRelationsAttributesMapList:
                                        for j in range(0, len(complexRelationsAttributesMap['attributeReferences']['attributeReference'])):
                                            attributesReferenceList = complexRelationsAttributesMap['attributeReferences']['attributeReference'][j]
                                            attributeKey = attributesReferenceList['labelReference']['signifier']
                                            attributeValue.append(cleanhtml(attributesReferenceList['value']))
                                            if attributeKey in targetDataComplexRelationsAttributesMap.keys():
                                                tempList = targetDataComplexRelationsAttributesMap[attributeKey]
                                                attributeValue = attributeValue + tempList
                                            targetDataComplexRelationsAttributesMap[attributeKey] = attributeValue
                                            attributeValue = []

                                    targetDataComplexRelationsMap['Attributes'] = targetDataComplexRelationsAttributesMap
                        tempMap = {}
                        finalMap['Asset Details'] = targetDataMap
                        finalMap['Attributes'] = targetDataAttributesMap
                        finalMap['Relations'] = targetDataRelationsMap
                        finalMap['Complex Relations'] = targetDataComplexRelationsMap
                        finalResultList.append(finalMap)
                        finalMap = {}
                else:
                    print('relationPath')
            elif itemkey == 'outputFileName':
                outputFileName = eachMap[itemkey]
                if outputFilter != 'relationPath':
                    # Create the output file
                    fileName = CreateDataFile.createDataFile(finalResultList, outputFileName, '.xlsx')
                    if fileName not in fileNameList:
                       fileNameList.append(fileName)
            elif itemkey == 'email':  #Emails the output file to the audience

                print('Hello')
                # zipFilePath = "K:/Git Code/Python/Output/" + outputFileName + ".zip"
                # os.chdir("K:/Git Code/Python/Output/")
                # for file in fileNameList:
                #     with ZipFile(zipFilePath, 'a') as myzip:
                #         myzip.write(os.path.basename(file))
                #     myzip.close()
                #
                # composedMessage = MIMEMultipart()
                # composedMessage['Subject'] = 'Requested Information'
                # composedMessage['To'] = eachMap[itemkey]
                # composedMessage['From'] = "srikrishna.bingi@gmail.com"
                #
                # ctype, encoding = mimetypes.guess_type(zipFilePath)
                # if ctype is None or encoding is not None:
                #     ctype = "application/octet-stream"
                #
                # zipFile = open(zipFilePath, 'rb')
                # maintype, subtype = ctype.split("/", 1)
                # msg = MIMEBase(maintype, _subtype=subtype)
                # msg.set_payload(zipFile.read())
                # encoders.encode_base64(msg)
                #
                # msg.add_header("Content-Disposition", "attachment", filename=outputFileName+'.zip')
                # composedMessage.attach(msg)

                # mailObject = smtplib.SMTP('smtp.gmail.com', 587)
                # mailObject.starttls()
                # mailObject.login('srikrishna.bingi@gmail.com','******')
                #mailObject.sendmail("srikrishna.bingi@gmail.com","srikrishna.bingi@exusia.com",composedMessage.as_string())
                print('Done sending Mail')