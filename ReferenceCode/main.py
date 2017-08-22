#!/usr/bin/env python

import requests
import sys
import APIMethod as api
import logging
import Error as er
from community import Community

import csv
my_logger = logging.getLogger('Collibra')
i=0
f=open('community list.txt','r+')
row=csv.reader(f,delimiter=',')
listOfAcceptedCommunities=list()
listOfRejecteCommunities=list()
for line in row:
    tempTuple=tuple()
    i=i+1
    name=line[0].strip()
    description=line[1].strip()
    parentName=line[2].strip()
    if Community.communityFind(name).statusCode==1:
        if not parentName or Community.communityFind(parentName).statusCode==0:
            c1 = Community(name, desc=description, parent=parentName)
            c1.postCommunity()
            c2=Community.communityFind(name)
            tempTuple=(name,c2.uri,c2.rid)
            listOfAcceptedCommunities.append(tempTuple)
        else:
            tempTuple=(name,'No','No')
            listOfRejecteCommunities.append(tempTuple)
    else:
        tempTuple = (name, 'Yes', 'NA')
        listOfRejecteCommunities.append(tempTuple)

for iTemp in listOfAcceptedCommunities:
    print('Accept List:',iTemp[0],iTemp[1],iTemp[2])


for iTemp in listOfRejecteCommunities:
    print('Reject List:',iTemp[0],iTemp[1],iTemp[2])



