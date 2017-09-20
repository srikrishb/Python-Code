import APIMethod as APIFile

class Asset:

    def __init__(self, resourceId):
        self.resourceId = resourceId

    @staticmethod
    def getDataCall(endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin

    @staticmethod
    def fetchDataSet(innerMapKey, innerMapValue):

        result = dict()
        if str.upper(innerMapKey).find('COMPLEXRELATIONNAME') != -1 or str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1 or str.upper(innerMapKey).find('RELATIONTYPEIN') != -1 or str.upper(innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find("CREATED") != -1 or str.upper(innerMapKey).find('ASSETNAMEIN') != -1 or str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1:
            searchSignfier = ''
        elif str.upper(innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS':
            searchSignfier = innerMapValue

        if str.upper(innerMapKey).find('COMPLEXRELATIONNAME') != -1 or str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1 or str.upper(innerMapKey).find('RELATIONTYPEIN') != -1 or str.upper(innerMapKey).find('ATTRIBUTETYPE') != -1 or str.upper(innerMapKey) == 'ASSETNAMEIN' or str.upper(innerMapKey) == 'ASSETNAMELIKE' or str.upper(innerMapKey) == 'ASSETNAMEEQUALS' or str.upper(innerMapKey).find("LASTMODIFIED") != -1 or str.upper(innerMapKey).find("CREATED") != -1:
            assetNameLikeEndpoint = 'term/find/full'
            assetNameLikePayload = {'excludeMeta': 'false', 'searchSignifier': searchSignfier}
            assetNameLikeResponse = Asset.getDataCall(assetNameLikeEndpoint, assetNameLikePayload)

            if assetNameLikeResponse['statusCode'] == '1':
                result = assetNameLikeResponse['data']['term']

        return result

    # Fetches possible relations types and attributes types of an asset
    def fetchPossibleRelationsTypesAndAttributesTypes(self):
        possibleRandAEndpoint = 'concept_type/' + self.resourceId + '/possible_attribute_relation_types'
        possibleRandAPayload = ''
        possibleRandAResponse = self.getDataCall(possibleRandAEndpoint, possibleRandAPayload)
        if possibleRandAResponse['statusCode'] == '1':
            return possibleRandAResponse['data']
        else:
            return 'No Data Found'

    # Fetches possible attributes types of an asset
    def fetchPossibleAttributesTypes(self):
        possibleRandAEndpoint = 'concept_type/' + self.resourceId + '/possible_attribute_types'
        possibleRandAPayload = ''
        possibleRandAResponse = self.getDataCall(possibleRandAEndpoint, possibleRandAPayload)
        if possibleRandAResponse['statusCode'] == '1':
            return possibleRandAResponse['data']
        else:
            return 'No Data Found'

    # Fetches relations of an asset
    def fetchRelations(self):
        relationsResponseList = []

        sourceError = 'true'
        targetError = 'true'

        sourceRelationsEndpoint = 'concept_type/' + self.resourceId + '/source_relations'
        sourceRelationsPayload = ''
        sourceRelationsResponse = self.getDataCall(sourceRelationsEndpoint, sourceRelationsPayload)
        if sourceRelationsResponse['statusCode'] == '1':
            relationsResponseList.append(sourceRelationsResponse['data'])
        else:
            sourceError = 'No Data Found'

        targetRelationsEndpoint = 'concept_type/' + self.resourceId + '/target_relations'
        targetRelationsPayload = ''
        targetRelationsResponse = self.getDataCall(targetRelationsEndpoint, targetRelationsPayload)
        if targetRelationsResponse['statusCode'] == '1':
            relationsResponseList.append(targetRelationsResponse['data'])
        else:
            targetError = 'No Data Found'

        if sourceError == 'true' and targetError == 'true':
            return relationsResponseList
        else:
            return 'No Data Found'

    # Fetches attributes of an asset
    def fetchAttributes(self):
        attributesEndpoint = 'concept_type/' + self.resourceId + '/attributes'
        attributesPayload = ''
        attributesResponse = self.getDataCall(attributesEndpoint, attributesPayload)

        if attributesResponse['statusCode'] == '1':
            return attributesResponse['data']

    # Fetches complex relations of an asset
    def fetchComplexRelations(self):
        complexRelationsResponseList = []
        complexRelationsError = ''
        complexRelationDefinitionEndpoint = 'complex_relation/'
        complexRelationDefinitionPayload = {'term': self.resourceId}
        complexRelationDefinitionResponse = Asset.getDataCall(complexRelationDefinitionEndpoint,complexRelationDefinitionPayload)

        if complexRelationDefinitionResponse['statusCode'] == '1':
            complexRelationDefinitionData = complexRelationDefinitionResponse['data']
            if len(complexRelationDefinitionData['termReference']) == 0:
                return 'No Relations Found'
            else:
                complexRelationList = complexRelationDefinitionData['termReference']

                for complexRelation in complexRelationList:
                    complexRelationRelationsEndpoint = 'complex_relation/' + complexRelation[
                        'resourceId'] + '/relations'
                    complexRelationRelationsPayload = ''
                    complexRelationRelationsResponse = Asset.getDataCall(complexRelationRelationsEndpoint,complexRelationRelationsPayload)
                    if complexRelationRelationsResponse['statusCode'] == '1':
                        complexRelationsResponseList.append(complexRelationRelationsResponse['data'])
                    else:
                        complexRelationsError = 'No Data Found'

            if complexRelationsError == '':
                return complexRelationsResponseList
            else:
                return complexRelationsError