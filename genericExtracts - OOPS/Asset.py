#!/usr/bin/ python

import os
import sys
import APIMethod as APIFile
import math
import time

class Asset:

    def __init__(self,name,community,domain,assetType,resourceId):
        self.name=name
        self.community=community
        self.domain=domain
        self.assetType=assetType
        self.resourceId=resourceId

    def getDataCall(self, endpoint, payload):
        # Kickoff the workflow using the endpoint and payload
        trylogin = APIFile.API.getCall(endpoint, payload)
        return trylogin

    def convertEpochTime(inputTime):

        mathTargetTime = math.ceil(int(inputTime) / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mathTargetTime))

    def fetchAssetAssetDetails(self, detailType, targetData):

        if detailType == 'Asset Name':
            return targetData['signifier']

        if detailType == 'Community':
            if 'vocabularyReference' in targetData:
                if 'communityReference' in targetData['vocabularyReference']:
                    if 'name' in targetData['vocabularyReference']['communityReference']:
                        return targetData['vocabularyReference']['communityReference']['name']
                    else:
                        return 'Not Applicable'
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Domain':
            if 'vocabularyReference' in targetData:
                if 'name' in targetData['vocabularyReference']:
                    return targetData['vocabularyReference']['name']
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Asset Type':
            if 'conceptType' in targetData:
                if 'signifier' in targetData['conceptType']:
                    return targetData['conceptType']['signifier']
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Status':
            if 'statusReference' in targetData:
                if 'signifier' in targetData['statusReference']:
                    # targetDataMap['Status'] = targetData[i]['statusReference']['signifier']
                    return targetData[i]['statusReference']['signifier']
                else:
                    return 'Not Applicable'
            else:
                return 'Not Applicable'

        if detailType == 'Articulation Score':
            return targetData.get('articulation', 'Not Applicable')

        if detailType == 'Created On':
            return convertEpochTime(targetData.get('createdOn'))
        else:
            return 'Not Applicable'

        if detailType == 'Created By':
            return targetData['createdBy']['firstName'] + targetData['createdBy']['lastName']
        else:
            return 'Not Applicable'

        if detailType == 'Last Modified':
            return convertEpochTime(targetData.get('lastModified'))
        else:
            return 'Not Applicable'

        if detailType == 'Last Modified By':
            return targetData['lastModifiedBy']['firstName'] + targetData['lastModifiedBy']['lastName']
        else:
            return 'Not Applicable'