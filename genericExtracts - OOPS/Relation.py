import APIMethod as APIFile

class Relation:

    def __init__(self, resourceId):
        self.resourceId = resourceId

    def __init__(self):
        pass

    @staticmethod
    def getDataCall(endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin

    def fetchRelations(self, assetResourceId):
        relationsResponseList = []

        sourceError = 'true'
        targetError = 'true'

        sourceRelationsEndpoint = 'concept_type/' + assetResourceId + '/source_relations'
        sourceRelationsPayload = ''
        sourceRelationsResponse = Relation.getDataCall(sourceRelationsEndpoint, sourceRelationsPayload)
        if sourceRelationsResponse['statusCode'] == '1':
            relationsResponseList.append(sourceRelationsResponse['data'])
        else:
            sourceError = 'No Data Found'

        targetRelationsEndpoint = 'concept_type/' + assetResourceId + '/target_relations'
        targetRelationsPayload = ''
        targetRelationsResponse = Relation.getDataCall(targetRelationsEndpoint, targetRelationsPayload)
        if targetRelationsResponse['statusCode'] == '1':
            relationsResponseList.append(targetRelationsResponse['data'])
        else:
            targetError = 'No Data Found'

        if sourceError == 'true' and targetError == 'true':
            return relationsResponseList
        else:
            return 'No Data Found'