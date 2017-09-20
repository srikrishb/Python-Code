from Asset import Asset
import math
import time

class CreateMap:

    def __init__(self, inputMap):
        self.inputMap = inputMap

    # Static Method to add two lists and return the result
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

    # Static Method to find the intersection between two lists and return the result
    @staticmethod
    def listIntersect(refList, dataList):
        return set(refList).intersection(dataList)

    # Static Method to check whether a map has any nested 'OR' or 'AND' conditions
    @staticmethod
    def checkNestedMaps(checkMap):
        keyList = []

        for innerMap in checkMap:
            keyList.append(innerMap)

        if 'Or' in keyList or 'And' in keyList:
            return 1
        else:
            return 0

    # Static Method to convert EPOCH to GMT
    @staticmethod
    def convertEpochTime(inputTime):

        mathTargetTime = math.ceil(int(inputTime) / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))

    # Static Method to filter the results for a specified condition
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

        return filteredData

    # Static Method to generate results for given input
    @staticmethod
    def generateMap(inputMap):
        i = 0
        tempMap = {}
        for masterKey in inputMap:
            toBeProcessedMap = inputMap[masterKey]
            if isinstance(toBeProcessedMap, dict):
                for innerMapKey in toBeProcessedMap:
                    if masterKey == 'Or' or masterKey == 'And':
                        tempMap[innerMapKey] = toBeProcessedMap[innerMapKey]
                        # if innerMapKey == 'attributeFilter':
                        #     tempTargetData = CreateMap.fetchAttributeFilterDataSet(tempMap)
                        # else:
                        tempTargetData = Asset.fetchDataSet(innerMapKey, toBeProcessedMap[innerMapKey])

                        if i == 0:
                            i += 1
                            preTargetData = CreateMap.filterTargetData(tempMap, tempTargetData)
                        else:

                            if innerMapKey == 'attributeFilter':
                                newTargetData = tempTargetData
                            else:
                                newTargetData = CreateMap.filterTargetData(tempMap, tempTargetData)

                            if masterKey == 'And':
                                targetData = CreateMap.listIntersect(newTargetData, preTargetData)

                            if masterKey == 'Or':
                                targetData = CreateMap.listUnion(newTargetData, preTargetData)

                            preTargetData = targetData

                        tempMap = {}

            elif isinstance(toBeProcessedMap, str) or isinstance(toBeProcessedMap, list):
                tempTargetData = Asset.fetchDataSet(masterKey, inputMap[masterKey])
                targetData = CreateMap.filterTargetData(inputMap, tempTargetData)

        return targetData

    def createMap(self):
        tempMap = {}
        for key in self.inputMap:
            if self.checkNestedMaps(self.inputMap[key]) == 0:
                tempMap[key] = self.inputMap[key]
                targetData = self.generateMap(tempMap)
                tempMap = {}

        return targetData