import APIMethod as APIFile
import csv
import re

class ProcessElasticsearch:

    def __init__(self, index, docType, inputFile):
        self.index = index
        self.docType = docType
        self.inputFile = inputFile

    @staticmethod
    def postData(payload):
        response = APIFile.API.postSessionDataCall('/_bulk?', payload)

        if response['statusCode'] == '1':
            return response['data']
        else:
            return 'Issue with parameters. Please check'

    def insertElastisearch(self):

        # Temporary variable to store row count
        totalRowCount = 0

        tempMap={}
        bodyMap = {}
        finalBody = """"""
        dataLine = {}

        with open(self.inputFile) as dataFile:
            row = csv.DictReader(dataFile)
            for line in row:
                for map in line:
                    if map != '':
                        dataLine[map] = line[map]

                totalRowCount +=1

                id=dataLine['id']

                tempMap['_index']=self.index
                tempMap['_type']=self.docType
                tempMap['_id']=dataLine['id']

                bodyMap['index'] = tempMap
                finalBody = finalBody + '\n' + str(bodyMap) + '\n' + str(dataLine)



        finalBody = finalBody + '\n'
        print(finalBody.replace("'",'"'))

        #ProcessElasticsearch.postData(finalBody.replace("'",'"'))


