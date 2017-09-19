import APIMethod as APIFile

class Asset:

    def __init__(self, resourceId):
        self.resourceId = resourceId

    def __init__(self):
        pass

    @staticmethod
    def getDataCall(endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin

    @staticmethod
    def fetchDataSet(innerMapKey, innerMapValue):

        result = dict()
        if str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1 or str.upper(innerMapKey).find('RELATIONTYPEIN') != -1 or str.upper(innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find("CREATED") != -1 or str.upper(innerMapKey).find('ASSETNAMEIN') != -1 or str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1:
            searchSignfier = ''
        elif str.upper(innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS':
            searchSignfier = innerMapValue

        if str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1 or str.upper(innerMapKey).find('RELATIONTYPEIN') != -1 or str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1 or str.upper(innerMapKey) == 'ASSETNAMEIN' or str.upper(innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS' or str.upper(innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find("CREATED") != -1:
            assetNameLikeEndpoint = 'term/find/full'
            assetNameLikePayload = {'excludeMeta': 'false', 'searchSignifier': searchSignfier}
            assetNameLikeResponse = Asset.getDataCall(assetNameLikeEndpoint, assetNameLikePayload)

            if assetNameLikeResponse['statusCode'] == '1':
                result = assetNameLikeResponse['data']['term']

        return result

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
                        tempTargetData = Asset.fetchDataSet(innerKey, '')
                        attributeKey = innerMap[innerKey]
                        preTargetData = filterTargetData(tempMap, tempTargetData)
                    else:
                        targetData = filterAssetData(attributeKey, tempMap, preTargetData)
                    tempMap = {}

        return targetData