import os
import sys
import json
from CreateDataFile import CreateDataFile
from Job import Job
import shutil
import yaml
from openpyxl import load_workbook
import redis

if __name__ == '__main__':

    # Find the Parameter File Name
    paramFileName = sys.argv[1]

    os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r', encoding='utf8') as yamlFile:
        paramFileData = yaml.load(yamlFile)

    tempMap = {}
    # Find the request number
    for paramFileKey in paramFileData.keys():
        eachMap = paramFileData[paramFileKey]
        # Fetch the inner conditions of the request
        for eachMapKey in eachMap.keys():
            if eachMapKey == 'outputResult':
                tempMap = eachMap[eachMapKey]
                for tempMapKey in tempMap.keys():
                    print('tempMapKey', tempMapKey)
                    inputJSONParameterFile = tempMap[tempMapKey]
                    # Open the parameter file of the business process
                    os.chdir("K:\Git Code\Python\ParameterFiles\Metrics")
                    with open(inputJSONParameterFile, 'r', encoding='utf8') as jsonFile:
                        inputParamFileData = json.load(jsonFile)

                    # Instantiate an object for Data File creation
                    createDataFileObj = CreateDataFile(json.dumps(inputParamFileData))

                    # Create an excel file for the specified parameters and fetch the Job ID that performed the above task
                    createDataFileResponse = createDataFileObj.postData('excel')

                    if createDataFileResponse == 'Issue with parameters. Please check':
                        print('Issue with Create Data File parameters. Please check')
                    else:
                        jobId = createDataFileResponse

                        print('JobId', jobId)

                        # Instantiate a Job Object
                        jobObj = Job(jobId)

                        # Fetch Job Details
                        jobResponse = jobObj.fetchJobDetails()

                        if jobResponse == 'Issue with parameters. Please check':
                            print('Issue with Job parameters. Please check')
                        else:
                            if jobResponse['state'] == 'ERROR':
                                print('Error in Job. Please check log.')
                            else:
                                jobStatus = 'RUNNING'
                                while jobStatus == 'RUNNING':
                                    jobResponse = jobObj.fetchJobDetails()
                                    jobStatus = jobResponse['state']

                                # Fetch the Job message and convert it to JSON
                                jobMessage = json.loads(jobResponse['message'])

                                # Go to Collibra Temp Directory and rename the file
                                os.chdir("C:/collibra_data/dgc/temp-files")
                                #                os.rename(jobMessage['id'], 'File.xlsx')
                                shutil.copyfile(jobMessage['id'], "K:/Git Code/Python/Output/File.xlsx")

                                # Open the data file
                                workbook = load_workbook("K:/Git Code/Python/Output/File.xlsx")
                                defaultSheet = workbook.active

                                # Kick start redis
                                redis_db = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
                                redis_db.flushall()
                                i=0
                                key = ''
                                offset = 2
                                prev_assettype = ''
                                curr_assettype = ''
                                prev_offset = 2
                                currAssetName = ''
                                prevAssetName = ''
                                keyList =[]
                                for row in defaultSheet.rows:
                                    if i == 0:
                                        i+=1
                                        for cellInRow in row:
                                            if cellInRow.value == 'AssetType':
                                                marker = cellInRow.col_idx
                                                #xy = coordinate_from_string(cell)  # returns ('A',4)
                                                #marker = column_index_from_string(xy[0])  # returns 1
                                                print('marker', marker)
                                    else:
                                        for cellInRow in row:
                                            if cellInRow.col_idx == 1:
                                                currAssetName = cellInRow.value
                                            if cellInRow.col_idx > 1 and cellInRow.col_idx < marker:
                                                if cellInRow.col_idx == 2:
                                                    key = cellInRow.value
                                                else:
                                                    key = key + ":" + cellInRow.value
                                            if cellInRow.col_idx == marker:
                                                key = key + ":" + cellInRow.value
                                                curr_assettype = cellInRow.value
                                                if prev_assettype == curr_assettype:
                                                    if prevAssetName == currAssetName:
                                                        offset = prev_offset
                                                    else:
                                                        offset += 1
                                                        prevAssetName = currAssetName
                                                else:
                                                    if prevAssetName != currAssetName:
                                                        offset =2
                                                        prev_offset = offset
                                                        prev_assettype = curr_assettype
                                                        prevAssetName = currAssetName
                                        print(key, offset-1, 1)
                                        keyList.append(key)

                                        # see what keys are in Redis

                                        redis_db.setbit(key, offset-1, 1)
                                        key = ''

                                for key in keyList:
                                    print(key, redis_db.bitcount(key))

