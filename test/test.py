for targetMap in targetMapList:
    for mainHeaderKey in targetMap.keys():
        subHeaderMap = targetMap[mainHeaderKey]

        if mainHeaderKey == 'Asset Details' or mainHeaderKey == 'Attributes' or mainHeaderKey == 'Relations' or mainHeaderKey == 'Complex Relations':

            for subHeaderKey in subHeaderMap.keys():

                if '->' in subHeaderKey:
                    targetFileHeader.append(subHeaderKey[subHeaderKey.index('->') + 3:])
                else:
                    targetFileHeader.append(subHeaderKey)
                print(subHeaderMap[subHeaderKey])
                targetFileRow.append(subHeaderMap[subHeaderKey])