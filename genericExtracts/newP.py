resultInnerAnd1 = []
conditionsPath = []

def performOperation(key, tempResult):
    print('')
    #Perform set operations.

    resultInnerAnd1 =

def operationInnerMap()

def computeOperationMap(filter):
    pathIndex = 0
    for key in filter.keys():
        filterCriteria = filter[key]
        pathIndex += 1
        if isinstance(filterCriteria, list):
            for eachItem in filterCriteria:
                innerKey  = eachItem.keys()
                #innerKey is 'And1' in first loop
                innerMap = eachItem[innerKey]
                #innerMap is assetNameLike - amortized... and lastmodifiedbefore in first loop ...
                keysInInnerMap = innerMap.keys()
                #keysInInnerMap consists of keys assetNameLike and lastmodifiedbefore
                if 'Or' not in keysInInnerMap and 'And' not in keysInInnerMap:
                    #pathIndex = 1
                    #innerkey = 'And1'
                    # innerMap is assetNameLike - amortized... and lastmodifiedbefore
                    tempList = []
                    tempList.append(pathIndex)
                    tempList.append(innerKey)
                    tempList.append(innerMap)
                    globalList.append(tempList)
                    #globallist = [ (1, innerKey, innerMap} ]

                innerKey  = eachItem.keys()
                #innerKey is 'And2' in second loop
                innerMap = eachItem[innerKey]
                #innerMap is Or - And .. , And - assetname .. , LMA ..
                keysInInnerMap = innerMap.keys()
                #keysInInnerMap consists of keys Or, And, LMA
                if 'Or' not in keysInInnerMap and 'And' not in keysInInnerMap:
                    #pathIndex = 1
                    #innerkey = 'And1'
                    # innerMap is assetNameLike - amortized... and lastmodifiedbefore
                    tempList = []
                    tempList.append(pathIndex)
                    tempList.append(innerKey)
                    tempList.append(innerMap)
                    globalList.append(tempList)
                    #globallist = [ (1, innerKey, innerMap} ]

                else:
                    computeOperationMap(innerMap)