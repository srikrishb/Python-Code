import requests
import logging
import CollibraError as ER
import os
import json


my_logger = logging.getLogger('Collibra')


class API:
    baseurl = ''
    useName = ''
    password = ''
    restversion = ''

    def __init__(self, baseurl):
        self.baseurl = baseurl
    statusCode=''
    responseData=''
    #
    # def getCall(args,payload):
    #     url = "%s/%s/%s" % (con.baseurl, con.restversion, args)
    #     r = requests.get(url, auth=(con.useName, con.password), params=payload)
    #     if r.status_code != 200:
    #             raise ER.CollibraGetException("Exception In Function getCall() For endPoint :"+args +" For URL "+ r.url+" For Argument :"+str(payload) +" Return Code Is " +str(r.status_code))
    #     j = r.json()
    #     targetFileName = 'K:/Git Code/Python/Output/content.json'
    #     targetFile = open(targetFileName, 'w', newline='')
    #     json.dump(r.json(), targetFile)
    #     return {'statusCode': '1', 'data': j}

    def getCall(args, payload):
        url = "%s%s" % (con.baseurl, args)

        r = requests.get(url, params=payload)

        if r.status_code != 200:
            raise ER.CollibraGetException(
                "Exception In Function getCall() For endPoint :" + args + " For URL " + r.url + " For Argument :" + str(
                    payload) + " Return Code Is " + str(r.status_code))
        j = r.json()

        targetFileName = 'K:/Git Code/Python/Output/content.json'
        targetFile = open(targetFileName, 'w', newline='')
        json.dump(r.json(), targetFile)

        return {'statusCode': '1', 'data': j}



    def postDataCall(args, payload):
        url = "%s/%s" % (con.baseurl, args)
        r = requests.post(url, data=payload)


        if ( (r.status_code != 201 and args == 'workflow') or (r.status_code != 200 and args != 'workflow') ) :
            #my_logger.debug("No Data Sync For " + str(payload))
            #return {'statusCode': '999', 'data': 'Add To Collibra Error'}
            raise ER.CollibraPostException("Exception In Function postCall() For endPoint :" + args + " For URL " + r.url + " For Argument :" + str(payload) + " Return Code Is " + str(r.status_code))

        if r.text == '' and r.status_code == 200:
            return {'statusCode': '1'}
        else:
            j = r.json()
            return {'statusCode': '1', 'data': j}

    @staticmethod
    def postSessionDataCall(args, payload):
        url = con.baseurl + args
        ses = requests.session()
        ses.get(url)
        ses.headers = {"Content-Type": "application/json"}
        r = ses.post(url, data=payload)

        print(r.text)
        if r.status_code == 200 or r.text == '':
            return {'statusCode': '1', 'data': r.text}
        else:
            return {'statusCode': '0'}

# Find the Parameter File Name
paramFileName = 'connectionParameters.json'

#Open the parameter file
os.chdir("/media/legolas/Softwares/Git Code/Python/Elasticsearch")
with open(paramFileName) as jsonfile:
    paramfiledata = json.load(jsonfile)

#Extract connection parameters from the file
baseurl = paramfiledata['URL']

con=API(baseurl)

