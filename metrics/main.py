import os
import sys
import json
from CreateDataFile import CreateDataFile
from Job import Job
import shutil
import yaml
from ProcessMetrics import ProcessMetrics

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
                                shutil.copyfile(jobMessage['id'], "K:/Git Code/Python/Output/"+paramFileKey+".xlsx")

                                processMetricsObj = ProcessMetrics( "K:/Git Code/Python/Output/"+paramFileKey+".xlsx")
                                processMetricsObj.generateMetricsFileII(tempMapKey, 'K:/Git Code/Python/Output/Metrics.xlsx')



