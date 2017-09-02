import APIMethod as APIFile

class AssetType:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def getDataCall(endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin

    def fetchDataSet(self, endpoint, payload):
        response = AssetType.getDataCall(endpoint, payload)
        if response['statusCode'] == '1':
            return response['data']['termReference']

    def filterAssetType(self, assetTypeDataSet, assetTypeName):
        for assetTypeData in assetTypeDataSet:
            if assetTypeData['signifier'] == assetTypeName:
                return assetTypeData['resourceId']
