from Asset import Asset
from Relation import Relation

class RelationFilter:

    def __init__(self, parameterList):
        self.parameterList = parameterList
        print(self.parameterList)

    def filterRelationDataSet(self, dataToBeFiltered):
        filteredData = []

        for data in dataToBeFiltered:
            #Fetch relations for the resourceId
            relationObj = Relation()
            assetRelationList = relationObj.fetchRelations(data['resourceId'])

            #Loop through each inner map in assetRelationList
            for relationMap in assetRelationList:
                # Extra relation map from inner relation list
                assetRelationInnerList = relationMap['relation']
                if len(assetRelationList) > 0 :
                    # Loop through assetRelationInnerList to find the relation
                    for innerRelationMap in  assetRelationInnerList:
                        role = innerRelationMap['typeReference']['role']
                        # Check whether relation type exists for an asset
                        for relationType in self.parameterList['RelationTypeIn']:
                            if role == relationType:
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
