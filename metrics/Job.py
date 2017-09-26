import APIMethod as APIFile

class Job:

    def __init__(self, jobId):
        self.jobId = jobId

    def fetchJobDetails(self):
        endpoint = "job/" + self.jobId
        payload = ''

        response = APIFile.API.getCall(endpoint, payload)
        if response['statusCode'] == '1':
            return response['data']
        else:
            return 'Issue with parameters. Please check'