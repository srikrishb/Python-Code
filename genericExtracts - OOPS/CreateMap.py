import APIMethod as APIFile
import AttributeFilter
import time
import math

class CreateMap:

    def __init__(self, inputMap):
        self.inputMap = inputMap

    @staticmethod
    def convertEpochTime(inputTime):

        mathTargetTime = math.ceil(int(inputTime) / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))

    @staticmethod
    def getDataCall(endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin

    @staticmethod
    def fetchDataSet(innerMapKey, innerMapValue):

        result = dict()
        if str.upper(innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find(
                "CREATED") != -1 or str.upper(innerMapKey).find('ASSETNAMEIN') != -1 or str.upper(innerMapKey).find(
                'ATTRIBUTETYPE') != -1:
            searchSignfier = ''
        elif str.upper(innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS':
            searchSignfier = innerMapValue

        if str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1 or str.upper(innerMapKey) == 'ASSETNAMEIN' or str.upper(
                innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS' or str.upper(
                innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find("CREATED") != -1:
            assetNameLikeEndpoint = 'term/find/full'
            assetNameLikePayload = {'excludeMeta': 'false', 'searchSignifier': searchSignfier}
            assetNameLikeResponse = CreateMap.getDataCall(assetNameLikeEndpoint, assetNameLikePayload)

            if assetNameLikeResponse['statusCode'] == '1':
                result = assetNameLikeResponse['data']['term']

        return result

    @staticmethod
    def listUnion(refList, dataList):

        newList = []
        newMap = refList

        for item in refList:
            newList.append(item['resourceId'])

        for items2 in dataList:
            if items2['resourceId'] not in newList:
                newMap.append(items2)

        return newMap

    @staticmethod
    def listIntersect(refList, dataList):

        return set(refList).intersection(dataList)

    @staticmethod
    def fetchPossibleAttributes(resourceId):
        possibleRandAEndpoint = 'concept_type/' + resourceId + '/possible_attribute_types'
        possibleRandAPayload = ''
        possibleRandAResponse = CreateMap.getDataCall(possibleRandAEndpoint, possibleRandAPayload)
        if possibleRandAResponse['statusCode'] == '1':
            return possibleRandAResponse['data']
        else:
            return 'No Data Found'

    @staticmethod
    def filterTargetData(innerMap, dataToBeFiltered):
        filteredData = []
        for key in innerMap.keys():

            filterValue = innerMap[key]

            if str.upper(key).find("LASTMODIFIED") != -1 or str.upper(key).find("CREATED") != -1:
                if str.upper(key).find("LASTMODIFIED") != -1:
                    lookupKey = 'lastModified'
                elif str.upper(key).find("CREATEDBEFORE") or key.find("CREATEDAFTER") or key.find(
                        "CREATEDBETWEEN") != -1:
                    lookupKey = 'createdOn'

                i = 0
                for data in dataToBeFiltered:

                    dateTargetTime = CreateMap.convertEpochTime(dataToBeFiltered[i][lookupKey])
                    if str.upper(key).find("AFTER") != -1:
                        if dateTargetTime > filterValue:
                            filteredData.append(data)
                    elif str.upper(key).find("BEFORE") != -1:
                        if dateTargetTime < filterValue:
                            filteredData.append(data)
                    elif str.upper(key).find("BETWEEN") != -1:

                        term1 = filterValue[0]
                        term2 = filterValue[1]
                        if dateTargetTime >= term1 and dateTargetTime <= term2:
                            filteredData.append(data)

                    i += 1
            elif str.upper(key).find("ASSETNAMELIKE") != -1:
                return dataToBeFiltered

            elif str.upper(key).find("ASSETNAMEEQUALS") != -1:
                i = 0
                for data in dataToBeFiltered:
                    if data['signifier'] == filterValue:
                        filteredData.append(data)
                    i += 1

            elif str.upper(key).find("ASSETNAMEIN") != -1:
                i = 0
                for filterItem in filterValue:
                    for data in dataToBeFiltered:
                        if data['signifier'] == filterItem:
                            filteredData.append(data)
                        i += 1

            elif str.upper(key).find("ATTRIBUTETYPE") != -1:
                i = 0
                for data in dataToBeFiltered:
                    # Find out whether there are any attributes tied to the asset:
                    possibleAttributesList = fetchPossibleAttributes(data['resourceId'])
                    if len(possibleAttributesList['attributeType']) > 0:
                        # Fetch attributes for the resourceId
                        attributesResponse = fetchAttributes(data['resourceId'])
                        attributesResponseList = attributesResponse['attributeReference']

                        # Loop through the attributesResponseList to check whether specified filterValue has been set
                        for listIndex in range(0, len(attributesResponseList)):
                            attributeResponseMap = attributesResponseList[listIndex]
                            attributeType = attributeResponseMap['labelReference']['signifier']
                            if attributeType == filterValue:
                                filteredData.append(data)
                        i += 1

        return filteredData

    @staticmethod
    def generateFile(inputMap):
        i = 0
        tempMap = {}
        print(inputMap)
        for masterKey in inputMap:
            toBeProcessedMap = inputMap[masterKey]
            if isinstance(toBeProcessedMap, dict):
                for innerMapKey in toBeProcessedMap:
                    if masterKey == 'Or' or masterKey == 'And':
                        tempMap[innerMapKey] = toBeProcessedMap[innerMapKey]

                        if i == 0:
                            i += 1
                            preTargetData = filterTargetData(tempMap, tempTargetData)

                        else:
                            newTargetData = filterTargetData(tempMap, tempTargetData)

                            if masterKey == 'And':
                                targetData = CreateMap.listIntersect(newTargetData, preTargetData)

                            if masterKey == 'Or':
                                targetData = CreateMap.listUnion(newTargetData, preTargetData)

                            preTargetData = targetData

                        tempMap = {}

            elif isinstance(toBeProcessedMap, str) or isinstance(toBeProcessedMap, list):
                tempTargetData = fetchDataSet(masterKey, inputMap[masterKey])
                targetData = filterTargetData(inputMap, tempTargetData)

        return targetData

    @staticmethod
    def checkNestedMaps(checkMap):
        keyList = []
        for innerMap in checkMap:
            keyList.append(innerMap)
        if 'Or' in keyList or 'And' in keyList:
            return 1
        else:
            return 0

    def createMapII(self):
        tempMap = {}
        for key in self.inputMap:
            if CreateMap.checkNestedMaps(self.inputMap[key]) == 0:
                tempMap[key] = self.inputMap[key]
                targetData = CreateMap.generateFile(tempMap)
                tempMap = {}

        return targetData