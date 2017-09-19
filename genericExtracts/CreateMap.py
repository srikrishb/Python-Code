from Asset import Asset

class CreateMap:

    def __init__(self, inputMap):
        self.inputMap = inputMap

    @staticmethod
    def generateFile(inputMap):
        i = 0
        tempMap = {}
        print(inputMap)
        for masterKey in inputMap:
            toBeProcessedMap = inputMap[masterKey]
            print(toBeProcessedMap, type(toBeProcessedMap))
            if isinstance(toBeProcessedMap, dict):
                for innerMapKey in toBeProcessedMap:
                    if masterKey == 'Or' or masterKey == 'And':
                        tempMap[innerMapKey] = toBeProcessedMap[innerMapKey]
                        if innerMapKey == 'attributeFilter':
                            tempTargetData = CreateMap.fetchAttributeFilterDataSet(tempMap)
                        else:
                            tempTargetData = Asset.fetchDataSet(innerMapKey, toBeProcessedMap[innerMapKey])

                        if i == 0:
                            i += 1
                            preTargetData = Asset.filterTargetData(tempMap, tempTargetData)
                        else:

                            if innerMapKey == 'attributeFilter':
                                newTargetData = tempTargetData
                            else:
                                newTargetData = filterTargetData(tempMap, tempTargetData)

                            if masterKey == 'And':
                                targetData = listIntersect(newTargetData, preTargetData)

                            if masterKey == 'Or':
                                targetData = listUnion(newTargetData, preTargetData)

                            preTargetData = targetData

                        tempMap = {}

            elif masterKey == 'attributeFilter':
                tempMap[masterKey] = inputMap[masterKey]
                targetData = Asset.fetchAttributeFilterDataSet(tempMap)
                tempMap = {}

            elif isinstance(toBeProcessedMap, str) or isinstance(toBeProcessedMap, list):
                tempTargetData = Asset.fetchDataSet(masterKey, inputMap[masterKey])
                targetData = filterTargetData(inputMap, tempTargetData)

        return targetData

    def createMapII(self):
        tempMap = {}
        for key in self.inputMap:
            if checkNestedMaps(self.inputMap[key]) == 0:
                tempMap[key] = inputMap[key]
                targetData = generateFile(tempMap)
                tempMap = {}

        return targetData