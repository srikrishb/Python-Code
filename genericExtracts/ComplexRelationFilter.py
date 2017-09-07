from ComplexRelation import ComplexRelation

class ComplexRelationFilter:

    def __init__(self, parameterList):
        self.parameterList = parameterList
        print(self.parameterList)

    def filterComplexRelationDataSet(self, dataToBeFiltered):
        filteredData = []

        for data in dataToBeFiltered:
            #Fetch relations for the resourceId
            complexRelationObj = ComplexRelation()
            assetComplexRelationMap = complexRelationObj.fetchComplexRelations(data['resourceId'])

            if assetComplexRelationMap != 'No Relations Found':
                #Loop through each inner map in assetComplexRelationMap
                for complexRelationMapList in assetComplexRelationMap['relationReference']:
                    # Extract complex relation map from inner complexRelationMap
                    if len(complexRelationMapList) > 0 :
                        complexRelationMap = complexRelationMapList['typeReference']
                        complexRelationHeadTerm = complexRelationMap['headTerm']
                        complexRelationName = complexRelationHeadTerm['signifier']
                        # Check whether complex relation type exists for an asset
                        if complexRelationName in self.parameterList['complexRelationName']:
                            if data not in filteredData:
                                filteredData.append(data)


        return filteredData

    def filterTargetDataSet(self, dataToBeFiltered):
        filteredData = []
        filterList = []

        for data in dataToBeFiltered:
            dataAssetType = data['conceptType']['signifier']
            if dataAssetType in self.parameterList['AssetType']:
                filteredData.append(data)

        return filteredData
