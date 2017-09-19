from Attribute import Attribute
import re

class AttributeFilter:

    def __init__(self, parameterMap):
        self.parameterMap = parameterMap
        print(self.parameterMap)

    @staticmethod
    def fetchAttributeFilterDataSet(inputMap):
        i = 0
        tempMap = {}
        for inputKey in inputMap:
            innerList = inputMap[inputKey]
            for innerMap in innerList:
                for innerKey in innerMap:
                    tempMap[innerKey] = innerMap[innerKey]
                    if i == 0:
                        i += 1
                        tempTargetData = Attribute.fetchDataSet(innerKey, '')
                        attributeKey = innerMap[innerKey]
                        preTargetData = Attribute.filterTargetData(tempMap, tempTargetData)
                    else:
                        targetData = Attribute.filterAssetData(attributeKey, tempMap, preTargetData)
                    tempMap = {}

        return targetData

    def filterAttributeDataSet(self, dataToBeFiltered):
        filteredData = []
        i = 0
        for data in dataToBeFiltered:
            # Find out whether there are any attributes tied to the asset:
            possibleAttributesList = Attribute.fetchPossibleAttributes(data['resourceId'])
            if len(possibleAttributesList['attributeType']) > 0:
                # Fetch attributes for the resourceId
                attributesResponse = Attribute.fetchAttributes(data['resourceId'])
                attributesResponseList = attributesResponse['attributeReference']

                # Loop through the attributesResponseList to check whether specified filterValue has been set
                for listIndex in range(0, len(attributesResponseList)):
                    attributeResponseMap = attributesResponseList[listIndex]
                    attributeType = attributeResponseMap['labelReference']['signifier']
                    if attributeType == self.parameterMap['attributeTypeEquals']:
                        filteredData.append(data)
                i += 1

        return filteredData

    def filterTargetDataSet(self, filterAttributeType, dataToBeFiltered):

        def cleanhtml(raw_html):
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', raw_html)
            cleantext = cleantext.replace(u'\xa0', u' ')
            return cleantext

        filteredData = []
        filterList = []

        for key in self.parameterMap.keys():
            filterValue = self.parameterMap[key]
            if str.upper(key).find("ATTRIBUTEVALUEEQUALS") != -1:
                for data in dataToBeFiltered:
                    # Find the resourceId
                    attributesResponse = dataToBeFiltered(data['resourceId'])
                    attributesResponseList = attributesResponse['attributeReference']

                    existingValue = []
                    # Loop through the attributesResponseList to check whether specified filterValue has been set
                    for listIndex in range(0, len(attributesResponseList)):
                        attributeResponseMap = attributesResponseList[listIndex]
                        # key = attributeResponseMap['resourceId'] + ' -> ' + attributeResponseMap['labelReference']['signifier']
                        attributeType = attributeResponseMap['labelReference']['signifier']
                        if attributeType == filterAttributeType:
                            cleanedValue = cleanhtml(attributeResponseMap['value'])
                            if cleanedValue == filterValue:
                                filteredData.append(data)

        return filteredData


