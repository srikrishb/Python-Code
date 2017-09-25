import os
import sys
import json
from CreateDataFile import CreateDataFile
from Job import Job

if __name__ == '__main__':

    # Find the Parameter File Name
    paramFileName = sys.argv[1]

    # Open the parameter file of the business process
    os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r', encoding='utf8') as jsonFile:
        paramFileData = json.load(jsonFile)

    # Instantiate an object for Data File creation
    createDataFileObj = CreateDataFile(json.dumps(paramFileData))

    # Create an excel file for the specified parameters and fetch the Job ID that performed the above task
    createDataFileResponse = createDataFileObj.postData()

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
                print(jobMessage['id'])

                # Go to Collibra Temp Directory and rename the file
                os.chdir("C:/collibra_data/dgc/temp-files")
                os.rename(jobMessage['id'], 'File.xlsx')