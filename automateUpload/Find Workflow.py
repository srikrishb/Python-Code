#!/usr/bin/ python

import os
import csv
import requests
import json

#Function helps in connecting to DGC instance
def dgcupload(baseurl, user, passw, jenkinstargetfolderpath, deltalistfile):

    endpoint = "community"
    payload = {'name': 'CCAR Reporting Community'}
    url = baseurl + endpoint
    # Open the file path
    os.chdir(jenkinstargetfolderpath)
    #payload = {'filename': deltalistfile}

    print(url)

    trylogin = requests.get(url, auth=(user, passw), params=payload)
    trylogin_json = trylogin.json()

    print(trylogin.text)
    print(trylogin_json["vocabularyReferences"]["vocabularyReference"])

    print(trylogin_json["vocabularyReferences"]["vocabularyReference"][0]['resourceId'])
    if trylogin.status_code == 401:
        print('Unable to login (' + trylogin.text + ')')
    elif trylogin.status_code == 200:
        print('Logged in successfully')

#Main function
if __name__ == '__main__':

    #Find the Parameter File Name
    paramFileName = 'automateUploadParam.txt'

    #Open the parameter file
    os.chdir("K:\Git Code\Python\ParameterFiles")
    paramfiledata = open(paramFileName,'r')
    paramfiledatarow = csv.reader(paramfiledata, delimiter=',')

    for line in paramfiledatarow:

        #Find position of ':'
        pos = line[0].find(':')

        #Extract the subject
        lineX = line[0]
        subject=lineX[0:pos]

        if subject == 'URL':
            baseurl = lineX[pos+1:len(lineX)]
        elif subject == 'User':
            user = lineX[pos+1:len(lineX)]
        elif subject == 'Pass':
            passw = lineX[pos+1:len(lineX)]
        elif subject == 'RestVersion':
            restversion = lineX[pos+1:len(lineX)]
        elif subject == 'JenkinsTargetFolder':
            jenkinstargetfolderpath = lineX[pos+1:len(lineX)]
        elif subject == 'DeltaListPath':
            deltalistpath = lineX[pos+1:len(lineX)]
        elif subject == 'DeltaListFile':
            deltalistfile = lineX[pos+1:len(lineX)]

    #Change to the folder where the files are present
    os.chdir(deltalistpath)
    deltalistdata = open(deltalistfile,'r')
    deltalistdatarow = csv.reader(deltalistdata)

    for line in deltalistdatarow:
        if line[0].endswith('.bpmn'):
            print(line[0])
            dgcupload(baseurl, user, passw, jenkinstargetfolderpath, line[0])