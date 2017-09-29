import re
from AttributeFilter import AttributeFilter
from RelationFilter import RelationFilter
from ComplexRelationFilter import ComplexRelationFilter
from Asset import Asset
from CreateMap import CreateMap
from CreateDataFile import CreateDataFile

class ProcessMaps:

    outputParameterList = []

    def __init__(self, inputMap):
        self.inputMap = inputMap

    @staticmethod
    def cleanhtml(raw_html):
      cleanr = re.compile('<.*?>')
      cleantext = re.sub(cleanr, '', raw_html)
      cleantext = cleantext.replace(u'\xa0', u' ')
      return cleantext


    def processMaps(self):

        targetData = ''
        outputFilter = ''
        fileNameList = []
        finalMap = {}
        finalResultList = []
        eachMap = self.inputMap
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
                    outputResultParameters = eachMap[itemkey]
                    for i in range(0, len(targetData)):
                        targetDataMap = {}
                        assetObj = Asset(targetData[i]['resourceId'])
                        for outputParameter in outputResultParameters.keys():

                            # targetDataMap['Status'] = targetData[i]['statusReference']['signifier']
                            if outputParameter == 'Asset Details':
                                ProcessMaps.outputParameterList = outputResultParameters[outputParameter]
                                for detailType in ProcessMaps.outputParameterList:
                                    targetDataMap[detailType] = assetObj.fetchAssetAssetDetails(detailType, targetData[i])

                        tempMap = {}
                        finalMap['Asset Details'] = targetDataMap
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

        return targetData

    @staticmethod
    def checkCompletion(inputAssetData):
        finalMap = {}
        finalResultList = []
        # Fetch Completion Status for all the assets
        for i in range(0, len(inputAssetData)):

            targetDataMap = {}
            assetObj = Asset(inputAssetData[i]['resourceId'])
            for detailType in ProcessMaps.outputParameterList:
                targetDataMap[detailType] = assetObj.fetchAssetAssetDetails(detailType, inputAssetData[i])

            # Find possible attributes types and relations types
            possibleRelationsAndAttributesResponse = assetObj.fetchPossibleRelationsTypesAndAttributesTypes()
            possibleAttributeTypesList = []
            possibleRelationTypesList = []

            if possibleRelationsAndAttributesResponse != 'No Data Found':
                possibleRelationsAndAttributesList = possibleRelationsAndAttributesResponse['representationReference']
                for k in range(0, len(possibleRelationsAndAttributesList)):
                    if 'descriptionReference' in possibleRelationsAndAttributesList[k].keys():
                        possibleAttributeTypesList.append(possibleRelationsAndAttributesList[k]['signifier'])

                    if 'role' in possibleRelationsAndAttributesList[k].keys():
                        if possibleRelationsAndAttributesList[k]['role'] not in possibleRelationTypesList:
                            possibleRelationTypesList.append(possibleRelationsAndAttributesList[k]['role'])
                        if possibleRelationsAndAttributesList[k]['coRole'] not in possibleRelationTypesList:
                            possibleRelationTypesList.append(possibleRelationsAndAttributesList[k]['coRole'])
            completion = 'Y'
            # Fetch relation types that have been defined for an asset
            targetDataRelationsList = []
            relationsResponse = assetObj.fetchRelations()
            if relationsResponse != 'No Data Found':
                # Add all the relation types that have a value
                for relationResponseMap in relationsResponse:
                    for innerRelationsMap in relationResponseMap['relation']:
                        if 'vocabularyReference' in innerRelationsMap['typeReference']['headTerm']:
                            relationType = innerRelationsMap['typeReference']['headTerm']['vocabularyReference']['name']

                        if relationType != 'Complex Relation Types':
                            targetDataRelationsList.append(innerRelationsMap['typeReference']['role'])
                            targetDataRelationsList.append(innerRelationsMap['typeReference']['coRole'])

                # Determine whether all relation types have been defined
                for possibleRelationType in possibleRelationTypesList:
                        if possibleRelationType not in targetDataRelationsList:
                            targetDataMap['Completion-Category'] = 'N'
                            completion = 'N'
                            break

            # Fetch attributes types that have been defined for an asset
            if completion == 'Y':
                targetDataAttributesList = []
                attributesResponse = assetObj.fetchAttributes()
                if attributesResponse != 'No Data Found':
                    attributesResponseList = attributesResponse['attributeReference']

                    for listIndex in range(0, len(attributesResponseList)):
                        attributeResponseMap = attributesResponseList[listIndex]
                        key = attributeResponseMap['labelReference']['signifier']
                        if key not in targetDataAttributesList:
                            targetDataAttributesList.append(key)

                    # Add all the attribute types that don't have a value
                    for possibleAttribute in possibleAttributeTypesList:
                        if possibleAttribute not in targetDataAttributesList:
                            targetDataMap['Completion-Category'] = 'N'
                            completion = 'N'
                            break

            if 'Completion-Category' not in targetDataMap.keys():
                targetDataMap['Completion-Category'] = 'Y'

            finalMap['Asset Details'] = targetDataMap
            finalResultList.append(finalMap)
            finalMap = {}


        #Print the results to a file
        fileName = CreateDataFile.createDataFile(finalResultList, 'Detailed-Completion-Category', '.xlsx')
        return fileName