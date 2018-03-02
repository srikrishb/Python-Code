# -*- coding: utf-8 -*-
import sys
import yaml
from ProcessElasticsearch import ProcessElasticsearch
import time

if __name__ == '__main__':

    # Find the Parameter File Name
    paramFileName = sys.argv[1]

    #os.chdir("K:\Git Code\Python\ParameterFiles")
    with open(paramFileName, 'r') as yamlFile:
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

                if eachMapKey == 'server':
                    server = eachMap[eachMapKey]

                if eachMapKey == 'index':
                    indexName = eachMap[eachMapKey] + time.strftime("%m%d%Y")

                if eachMapKey == 'docType':
                    typeName = eachMap[eachMapKey]

                if eachMapKey == 'inputFile':
                    inputFile = eachMap[eachMapKey]

                if eachMapKey == 'tempFile':
                    tempFile = eachMap[eachMapKey]

                if eachMapKey == 'commitInterval':
                    commitInterval = eachMap[eachMapKey]

                if eachMapKey == 'alias':
                    alias = eachMap[eachMapKey]

            processElasticsearch = ProcessElasticsearch(server, indexName, typeName, inputFile, tempFile, commitInterval, alias)
            processElasticsearch.newInsertElastisearch()

            processElasticsearch.createAlias()
