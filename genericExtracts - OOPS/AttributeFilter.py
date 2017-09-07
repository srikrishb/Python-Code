
class AttributeFilter:

    def __init__(self):
        pass

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
                        tempTargetData = fetchDataSet(innerKey, '')
                        attributeKey = innerMap[innerKey]
                        preTargetData = filterTargetData(tempMap, tempTargetData)
                    else:
                        targetData = filterAssetData(attributeKey, tempMap, preTargetData)
                    tempMap = {}

        return targetData