#!/usr/bin/ python

import yaml

def createTuples(innerMap):

    for key in innerMap.keys():
        if key == 'Or' or key == 'And':

            filterCriteria = innerMap[key]
            if isinstance(filterCriteria, list):
                for item in filterCriteria:
                    createTuples(item)
            elif isinstance(filterCriteria, dict):
                createTuples(filterCriteria)
        else:
            print(key, innerMap[key])

def lastMap(innerMap):
    for key in innerMap.keys():
        filterCriteria = innerMap[key]
        if isinstance(filterCriteria, list):
            for item in filterCriteria:
                lastMap(item)
        elif isinstance(filterCriteria, dict):
            keyList = filterCriteria.keys()
            if 'Or' in keyList or 'And' in keyList:
                lastMap(filterCriteria)
            else:
                print(key, filterCriteria)
        elif isinstance(filterCriteria, str):
            print(key, filterCriteria)

def operationMap(filter):
    for key in filter.keys():
        filterCriteria = filter[key]
        if isinstance(filterCriteria, list):
            for eachItem in filterCriteria:
                operationMap(eachItem)
        elif isinstance(filterCriteria, dict):
            innerMapKeys = filterCriteria.keys()
            tempResult = []
            if 'Or' not in innerMapKeys or 'And' not in innerMapKeys:
                for eachKey in filterCriteria.keys():
                    innerMap = filterCriteria[eachKey]
                    tempResult.append(fetchResult(innerMap))
                resultInnerAnd1 = performOperation(key, tempResult)

if __name__ == '__main__':

    # Open the parameter file of the business process
    with open("K:\Git Code\Python\ParameterFiles\genericExtracts.yaml", 'r') as yamlFile:
       paramFileData = yaml.load(yamlFile)

    filter = paramFileData['request1']['conditions']
    createTuples(filter)


