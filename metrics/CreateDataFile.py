import APIMethod as APIFile

class CreateDataFile:

    def __init__(self, inputCriteria):
        self.inputCriteria = inputCriteria

    def postData(self, endpoint):

        fileEndpoint = 'output/' + endpoint
        payload = {'tableViewConfig': self.inputCriteria}

        response = APIFile.API.postSessionDataCall(fileEndpoint, payload)

        if response['statusCode'] == '1':
            return response['data']
        else:
            return 'Issue with parameters. Please check'