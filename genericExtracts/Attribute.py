import APIMethod as APIFile

class Attribute:

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
    def fetchAttributes(assetResourceId):
        attributesEndpoint = 'concept_type/' + assetResourceId + '/attributes'
        attributesPayload = ''
        attributesResponse = Attribute.getDataCall(attributesEndpoint, attributesPayload)

        if attributesResponse['statusCode'] == '1':
            return attributesResponse['data']

    @staticmethod
    def fetchPossibleAttributes(assetResourceId):
        possibleRandAEndpoint = 'concept_type/' + assetResourceId + '/possible_attribute_types'
        possibleRandAPayload = ''
        possibleRandAResponse = Attribute.getDataCall(possibleRandAEndpoint, possibleRandAPayload)
        if possibleRandAResponse['statusCode'] == '1':
            return possibleRandAResponse['data']
        else:
            return 'No Data Found'

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
            assetNameLikeResponse = Attribute.getDataCall(assetNameLikeEndpoint, assetNameLikePayload)

            if assetNameLikeResponse['statusCode'] == '1':
                result = assetNameLikeResponse['data']['term']