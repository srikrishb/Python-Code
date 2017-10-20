import os
import sys
import json
from CreateDataFile import CreateDataFile
from Job import Job
import shutil
import yaml
from ProcessMetrics import ProcessMetrics
from ProcessMaps import ProcessMaps
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

            if eachMapKey == 'Adoption-Category' or eachMapKey == 'Issue-Category':
                tempMap = eachMap[eachMapKey]
                for tempMapKey in tempMap.keys():
                    inputJSONParameterFile = tempMap[tempMapKey]
                    # Open the parameter file of the business process

                    if eachMapKey == 'Adoption-Category':
                        paramFilePath = "K:\Git Code\Python\ParameterFiles\Metrics"
                    else:
                        paramFilePath = "K:\Git Code\Python\ParameterFiles\Issues JSONs"

                    os.chdir(paramFilePath)
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

                                shutil.copyfile(jobMessage['id'], "K:/Git Code/Python/Output/Detailed-"+eachMapKey+"-"+tempMapKey+".xlsx")

                                processMetricsObj = ProcessMetrics("K:/Git Code/Python/Output/Detailed-"+eachMapKey+"-"+tempMapKey+".xlsx")
                                processMetricsObj.generateMetricsFileII(tempMapKey, 'K:/Git Code/Python/Output/Metrics-' + paramFileKey + '.xlsx')

            if eachMapKey == 'Completion-Category':
                # Fetch Assets basing on filter criteria
                tempMap = eachMap[eachMapKey]
                processMapsObj = ProcessMaps(tempMap)
                assetData = processMapsObj.processMaps()

                processMetricsObj = ProcessMetrics(processMapsObj.checkCompletion(assetData))
                processMetricsObj.generateMetricsFileII(eachMapKey,'K:/Git Code/Python/Output/Metrics-' + paramFileKey + '.xlsx')

            if eachMapKey == 'Process-Category':
                # Fetch Assets basing on filter criteria
                tempMap = eachMap[eachMapKey]
                processMapsObj = ProcessMaps(tempMap)
                assetData = processMapsObj.processMaps()

                processMetricsObj = ProcessMetrics(processMapsObj.checkProcess(assetData, paramFileKey))

            if eachMapKey == 'Activity-Category':
                # Fetch Assets basing on time difference
                timeDiff = eachMap[eachMapKey]

                processMapsObj = ProcessMaps(timeDiff)
                fetchLastViewedAssetsResponse = processMapsObj.fetchLastViewedAssets()
