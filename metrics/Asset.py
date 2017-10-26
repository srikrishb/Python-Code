import APIMethod as APIFile
import math
import time

class Asset:

    def __init__(self, resourceId):
        self.resourceId = resourceId

    # Issues a 'GET' operation to get data from Collibra
    @staticmethod
    def getDataCall(endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin

    # Fetches data specified for operation mentioned in 'innerMapKey' and operand mentioned in 'innerMapValue'
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

    # Converts EPOCH to EST
    @staticmethod
    def convertEpochTime(inputTime):
        mathTargetTime = math.ceil(int(inputTime) / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))

    # Fetches details of asset for excel file export
    @staticmethod
    def fetchAssetAssetDetails(detailType, targetData):

        if detailType == 'Asset Name':
            return targetData['signifier']

        if detailType == 'Community':
            if 'vocabularyReference' in targetData:
                if 'communityReference' in targetData['vocabularyReference']:
                    if 'name' in targetData['vocabularyReference']['communityReference']:
                        return targetData['vocabularyReference']['communityReference']['name']
                    else:
                        return 'Not Applicable'
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Domain':
            if 'vocabularyReference' in targetData:
                if 'name' in targetData['vocabularyReference']:
                    return targetData['vocabularyReference']['name']
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Asset Type':
            if 'conceptType' in targetData:
                if 'signifier' in targetData['conceptType']:
                    return targetData['conceptType']['signifier']
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Status':
            if 'statusReference' in targetData:
                if 'signifier' in targetData['statusReference']:
                    # targetDataMap['Status'] = targetData[i]['statusReference']['signifier']
                    return targetData[i]['statusReference']['signifier']
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Articulation Score':
            return targetData.get('articulation', 'Not Applicable')

        if detailType == 'Created On':
            return Asset.convertEpochTime(targetData.get('createdOn'))
        else:
            return 'Not Applicable'

        if detailType == 'Created By':
            return targetData['createdBy']['firstName'] + targetData['createdBy']['lastName']
        else:
            return 'Not Applicable'

        if detailType == 'Last Modified':
            return Asset.convertEpochTime(targetData.get('lastModified'))
        else:
            return 'Not Applicable'

        if detailType == 'Last Modified By':
            return targetData['lastModifiedBy']['firstName'] + targetData['lastModifiedBy']['lastName']
        else:
            return 'Not Applicable'

    # Fetches possible relations types and attributes types of an asset
    def fetchPossibleRelationsTypesAndAttributesTypes(self):
        possibleRandAEndpoint = 'term/' + self.resourceId + '/possible_attribute_relation_types'
        possibleRandAPayload = ''
        possibleRandAResponse = self.getDataCall(possibleRandAEndpoint, possibleRandAPayload)
        if possibleRandAResponse['statusCode'] == '1':
            return possibleRandAResponse['data']
        else:
            return 'No Data Found'

    # Fetches possible attributes types of an asset
    def fetchPossibleAttributesTypes(self):
        possibleRandAEndpoint = 'term/' + self.resourceId + '/possible_attribute_types'
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

        sourceRelationsEndpoint = 'term/' + self.resourceId + '/source_relations'
        sourceRelationsPayload = ''
        sourceRelationsResponse = self.getDataCall(sourceRelationsEndpoint, sourceRelationsPayload)
        if sourceRelationsResponse['statusCode'] == '1':
            relationsResponseList.append(sourceRelationsResponse['data'])
        else:
            sourceError = 'No Data Found'

        targetRelationsEndpoint = 'term/' + self.resourceId + '/target_relations'
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
        attributesEndpoint = 'term/' + self.resourceId + '/attributes'
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
                    complexRelationRelationsEndpoint = 'complex_relation/' + complexRelation['resourceId'] + '/relations'
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

    # Fetches attributes of complex relations of an asset
    def fetchComplexRelationsAttributes(self):
        complexRelationsResponseList = []
        complexRelationsError = ''
        complexRelationDefinitionEndpoint = 'complex_relation/'
        complexRelationDefinitionPayload = {'term': self.resourceId}
        complexRelationDefinitionResponse = Asset.getDataCall(complexRelationDefinitionEndpoint,complexRelationDefinitionPayload)

        if complexRelationDefinitionResponse['statusCode'] == '1':
            complexRelationDefinitionData = complexRelationDefinitionResponse['data']
            if len(complexRelationDefinitionData['termReference']) == 0:
                return 'No Attributes Found'
            else:
                complexRelationAttributesEndpoint = 'complex_relation/' + complexRelationDefinitionData['termReference'][0]['resourceId']
                complexRelationAttributesPayload = ''
                complexRelationAttributesResponse = Asset.getDataCall(complexRelationAttributesEndpoint,complexRelationAttributesPayload)
                if complexRelationAttributesResponse['statusCode'] == '1':
                    complexRelationsResponseList.append(complexRelationAttributesResponse['data'])
                else:
                    complexRelationsError = 'No Data Found'

        if complexRelationsError == '':
            return complexRelationsResponseList
        else:
            return complexRelationsError

    # Fetches processes tagged to an asset
    def fetchProcesses(self):
        processesResponseList = []
        processDefinitionEndpoint = 'term/' + self.resourceId + '/workflows'
        processDefinitionPayload = ''
        processDefinitionResponse = Asset.getDataCall(processDefinitionEndpoint,
                                                      processDefinitionPayload)

        if processDefinitionResponse['statusCode'] == '1':
            processDefinitionData = processDefinitionResponse['data']
            if len(processDefinitionData['workflowDefinition']) == 0:
                return 'No workflows Found'
            else:
                processList = processDefinitionData['workflowDefinition']

                for processMap in processList:
                    processesResponseList.append(processMap['processId'])

                return processesResponseList

        return 'No Data Found'

