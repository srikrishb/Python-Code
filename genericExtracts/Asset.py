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

    def fetchDataSet(self, endpoint, payload):
        response = Asset.getDataCall(endpoint, payload)
        if response['statusCode'] == '1':
            return response['data']['term']
