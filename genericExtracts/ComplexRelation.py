import APIMethod as APIFile

class ComplexRelation:

    def __init__(self, resourceId):
        self.resourceId = resourceId

    def __init__(self):
        pass

    @staticmethod
    def getDataCall(endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin


    def fetchComplexRelations(self, assetResourceId):
        complexRelationDefinitionEndpoint = 'complex_relation/'
        complexRelationDefinitionPayload = {'term': assetResourceId}
        complexRelationDefinitionResponse = ComplexRelation.getDataCall(complexRelationDefinitionEndpoint, complexRelationDefinitionPayload)

        if complexRelationDefinitionResponse['statusCode'] == '1':
            complexRelationDefinitionData = complexRelationDefinitionResponse['data']
            if len(complexRelationDefinitionData['termReference']) == 0:
                return 'No Relations Found'
            else:
                complexRelationRelationsEndpoint = 'complex_relation/' + complexRelationDefinitionData['termReference'][0]['resourceId'] + '/relations'
                complexRelationRelationsPayload = ''
                complexRelationRelationsResponse = ComplexRelation.getDataCall(complexRelationRelationsEndpoint,complexRelationRelationsPayload)
                if complexRelationRelationsResponse['statusCode'] == '1':
                    return complexRelationRelationsResponse['data']
                else:
                    return 'No Data Found'