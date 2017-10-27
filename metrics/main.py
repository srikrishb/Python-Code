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

    #os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r', encoding='utf8') as yamlFile:
        paramFileData = yaml.load(yamlFile)

    tempMap = {}
    # Find the request number
    for paramFileKey in paramFileData.keys():
        if paramFileKey == 'collibraTempFolder':
            collibraTempFolder = paramFileData[paramFileKey]
        if paramFileKey == 'outputFolder':
            outputFolder = paramFileData[paramFileKey]
        eachMap = paramFileData[paramFileKey]
        # Fetch the inner conditions of the request
        if isinstance(eachMap, dict):
            for eachMapKey in eachMap.keys():
                if eachMapKey == 'Adoption-Category' or eachMapKey == 'Issue-Category' or eachMapKey == 'Quality-Category':
                    tempMap = eachMap[eachMapKey]
                    for tempMapKey in tempMap.keys():
                        inputJSONParameterFile = tempMap[tempMapKey]
                        if tempMapKey != 'Metrics':
                            dimension = tempMapKey
                            # Open the parameter file of the business process
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
                                        os.chdir(collibraTempFolder)

                                        detailedFile = outputFolder + paramFileKey + "-Detailed-" + eachMapKey + "-" + tempMapKey+".xlsx"
                                        shutil.copyfile(jobMessage['id'], detailedFile)
                        if tempMapKey == 'Metrics':
                            metricMode = tempMap[tempMapKey]
                            processMetricsObj = ProcessMetrics(detailedFile)
                            metricsFile = outputFolder + paramFileKey + "-Metrics-" + eachMapKey + ".xlsx"
                            processMetricsObj.generateMetricsFileII(dimension, metricMode, metricsFile)

                if eachMapKey == 'Completion-Category' or eachMapKey == 'Process-Category':
                    # Read the Filter Criteria and the metrics display mode
                    innerMap = eachMap[eachMapKey]

                    # Loop through the map entries
                    for innerMapKey in innerMap.keys():

                        # Generate the detailed file for specified filter criteria
                        if innerMapKey == 'FilterCriteria':
                            # Fetch Assets basing on filter criteria
                            tempMap = innerMap[innerMapKey]
                            processMapsObj = ProcessMaps(tempMap)

                            # Generate detailed file basing on input criteria
                            if eachMapKey == 'Completion-Category':
                                detailedFile = outputFolder + paramFileKey + "-Detailed-" + eachMapKey + ".xlsx"
                                assetData = processMapsObj.processMaps(detailedFile)
                                processMetricsObj = ProcessMetrics(processMapsObj.checkCompletion(assetData, detailedFile))

                            elif eachMapKey == 'Process-Category':
                                detailedFile = outputFolder + paramFileKey + "-Detailed-" + eachMapKey + ".xlsx"
                                assetData = processMapsObj.processMaps(detailedFile)


                        # Generate metrics for the specified metric mode
                        if innerMapKey == 'Metrics':
                            metricMode = innerMap[innerMapKey]

                            # Create Metrics File using the detailed file generated in previous step
                            if eachMapKey == 'Completion-Category':
                                metricsFile = outputFolder + paramFileKey + "-Metrics-" + eachMapKey +  ".xlsx"
                                processMetricsObj.generateMetricsFileII(eachMapKey, metricMode, metricsFile)

                            elif eachMapKey == 'Process-Category':
                                metricsFile = outputFolder + paramFileKey + "-Metrics-" + eachMapKey + ".xlsx"
                                processMetricsObj = ProcessMetrics(processMapsObj.checkProcess(assetData, metricMode, detailedFile, metricsFile))

                if eachMapKey == 'Activity-Category':
                    # Fetch Assets basing on time difference
                    timeDiff = eachMap[eachMapKey]

                    detailedFile = outputFolder + paramFileKey + "-Detailed-" + eachMapKey + ".xlsx"
                    processMapsObj = ProcessMaps(timeDiff)
                    fetchLastViewedAssetsResponse = processMapsObj.fetchLastViewedAssets(detailedFile)
