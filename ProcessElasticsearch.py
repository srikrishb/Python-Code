# coding: utf-8
import csv
import APIMethod as APIFile
import datetime
import re
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time

class ProcessElasticsearch:

    def __init__(self, index, docType, inputFile, tempFile, commitInterval):
        self.index = index
        self.docType = docType
        self.inputFile = inputFile
        self.tempFile = tempFile
        self.commitInterval = commitInterval

    @staticmethod
    def postData(payload):
        response = APIFile.API.postSessionDataCall('/_bulk?', payload)

        if response['statusCode'] == '1':
            return response['data']
        else:
            return 'Issue with parameters. Please check'


    def oldinsertElastisearch(self):
        # Temporary variable to store row count
        rowCount = 0
        totalRowCount = 0

        startTime = datetime.datetime.now()

        print('starting process', startTime)

        idValue = ""
        finalBody = """"""
        dataLine = """{"""
        commaCount = 0

        with open(self.inputFile) as dataFile:
            # tempFile = open(self.tempFile, 'a')


            # Create CSV Dict Reader file object
            row = csv.DictReader(dataFile)

            # Count total number of rows:
            for tempLine in row:
                totalRowCount +=1

            dataFile.close()

        with open(self.inputFile) as dataFile:
            row = csv.DictReader(dataFile)

            # Read through the input file and insert data
            for line in row:
                bodyMap = """"""
                for key in line:
                    if key != '':
                        commaCount +=1
                        if commaCount < len(line.keys()) - 1:
                            dataLine = dataLine + """\"""" + key + "\"" + ":" + "\"" + re.sub('\n','', line[key]) + "\"" + ","
                        else:
                            dataLine = dataLine + """\"""" + key + "\"" + ":" + "\"" + re.sub('\n','', line[key]) + "\"" + "}"

                rowCount += 1

                idValue = line['id']
                bodyMap = """{ "index" : { "_index" : \"""" + self.index + """", "_type" : \"""" + self.docType +  """" , "_id" : \"""" + idValue + """"}}"""

                #finalBody = bodyMap + '\n' + str(dataLine)
                #tempFile.write(finalBody)

                if finalBody == """""":
                    finalBody = bodyMap + '\n' + str(dataLine)
                else:
                    finalBody = finalBody + '\n' + bodyMap + '\n' + str(dataLine)

                dataLine = """{"""
                commaCount = 0

                if rowCount ==  self.commitInterval or rowCount == totalRowCount:
                    print(rowCount, self.commitInterval, totalRowCount)
                    finalBody = finalBody + '\n'
                    response = ProcessElasticsearch.postData(finalBody)
                    finalBody == """"""


                    print(type(response))
                    if 'root_cause' in response:
                        print('Error in process. Please check.')
                    else:
                        print('Committed ',rowCount,' records. Please check')
                        print("\n")



                    rowCount = 0


        endTime = datetime.datetime.now()

        print('end of process', endTime)

        diffTime = endTime - startTime
        print('time elapsed in seconds', diffTime.seconds)

    def newInsertElastisearch(self):

        startTime = datetime.datetime.now()
        print('starting process', startTime)


        dataLine = """{"""
        commaCount = 0
        totalRowCount=0
        actions = []
        source = []
        bodyMap = """"""

        with open(self.inputFile) as dataFile:
            # tempFile = open(self.tempFile, 'a')


            # Create CSV Dict Reader file object
            row = csv.DictReader(dataFile)

            # Count total number of rows:
            for tempLine in row:
                totalRowCount +=1

            dataFile.close()

        with open(self.inputFile) as dataFile:

            row = csv.DictReader(dataFile)

            #Read through the input file and insert data
            for line in row:
                for key in line:
                    if key != '':
                        commaCount += 1
                        if commaCount < len(line.keys())-1:
                            dataLine = dataLine + """\"""" + key + "\"" + ":" + "\"" + re.sub('\n', '',line[key].replace('"',"'")) + "\"" + ","
                        else:
                            dataLine = dataLine + """\"""" + key + "\"" + ":" + "\"" + re.sub('\n', '',line[key].replace('"',"'")) + "\"" + "}"
                source.append(dataLine)
                dataLine="""{"""
                commaCount=0

        # for j in range(0, totalRowCount):
        #     bodyMap = """{ "index" : { "_index" : \"""" + self.index + """", "_type" : \"""" + self.docType + """" , "_id" : \"""" + str(j) + """" , "_source" : \"""" + source[j].decode('utf8') + """"}}"""
        #     actions.append(bodyMap)

        actions = [
            {
                "_index": self.index,
                "_type": self.docType,
                "_id": j,
                "_source": source[j].decode('utf8')
            }
            for j in range(0,len(source))

        ]

        es = Elasticsearch()

        helpers.bulk(es, actions)

        endTime = datetime.datetime.now()

        print('end of process', endTime)

        diffTime = endTime - startTime
        print('time elapsed in seconds', diffTime.seconds)