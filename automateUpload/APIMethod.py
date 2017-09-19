import requests
import logging
import CollibraError as ER
import os
import json
import http.client
import urllib.parse


my_logger = logging.getLogger('Collibra')


class API:
    baseurl = ''
    useName = ''
    password = ''
    restversion = ''

    def __init__(self, baseurl, useName, password, restversion):
        self.baseurl = baseurl
        self.useName = useName
        self.password = password
        self.restversion = restversion
    statusCode=''
    responseData=''

    def getCall(args,payload):
        url = "%s/%s/%s" % (con.baseurl, con.restversion, args)

        r = requests.get(url, auth=(con.useName, con.password), params=payload)
            #print(r.url)
        if r.status_code != 200:
            #my_logger.debug("No Data Found For "+str(payload))
            #return {'statusCode':'999','data':'No Data Available'}
                raise ER.CollibraGetException("Exception In Function getCall() For endPoint :"+args +" For URL "+ r.url+" For Argument :"+str(payload) +" Return Code Is " +str(r.status_code))
        j = r.json()
        return {'statusCode': '1', 'data': j}


    def postDataCall(args, payload):
        url = "%s/%s/%s" % (con.baseurl, con.restversion, args)
        r = requests.post(url, auth=(con.useName, con.password), data=payload)

        if ( (r.status_code != 201 and args == 'workflow') or (r.status_code != 200 and args != 'workflow') ) :
            #my_logger.debug("No Data Sync For " + str(payload))
            #return {'statusCode': '999', 'data': 'Add To Collibra Error'}
            raise ER.CollibraPostException("Exception In Function postCall() For endPoint :" + args + " For URL " + r.url + " For Argument :" + str(payload) + " Return Code Is " + str(r.status_code))

        if r.text == '' and r.status_code == 200:
            return {'statusCode': '1'}
        else:
            j = r.json()
            return {'statusCode': '1', 'data': j}


    def postSessionDataCall(args, payload):
        url = "%s/%s/%s" % (con.baseurl, con.restversion, args)
        ses = requests.session()
        ses.auth = (con.useName, con.password)
        ses.get(url)
        ses.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = ses.post(url, data=payload)

        if r.status_code == 200 or r.text == '':
            return {'statusCode': '1'}
        else:
            return {'statusCode': '0'}

    def postFileCall(args, payload):
        url = "%s/%s/%s" % (con.baseurl, con.restversion, args)
        r = requests.post(url, auth=(con.useName, con.password), files=payload)
        if r.status_code != 201:
            #my_logger.debug("No Data Sync For " + str(payload))
            #return {'statusCode': '999', 'data': 'Add To Collibra Error'}
            raise ER.CollibraPostException("Exception In Function postCall() For endPoint :" + args + " For URL " + r.url + " For Argument :" + str(payload) + " Return Code Is " + str(r.status_code))
        j = r.json()
        return {'statusCode': '1', 'data': j}

    def deleteCall(args, payload):
        url = "%s/%s/%s" % (con.baseurl, con.restversion, args)
        print (url)
        r = requests.delete(url, auth=(con.useName, con.password), data=payload)
        if r.status_code != 200:
            #my_logger.debug("No Data Sync For " + payload)
            #return {'statusCode': '999', 'data': 'Error Sync To Collibra'}
            raise ER.CollibraDelException("Exception In Function deleteCall() For endPoint :" + args + " For URL " + r.url + " For Argument :" + str(payload) + " Return Code Is " + str(r.status_code))
        j = r.json()
        return {'statusCode': '1', 'data': j}

# Find the Parameter File Name
paramFileName = 'connectionParameters.json'

#Open the parameter file
os.chdir("K:\Git Code\Python\ParameterFiles")
with open(paramFileName) as jsonfile:
    paramfiledata = json.load(jsonfile)

#Extract connection parameters from the file
baseurl = paramfiledata['URL']
user = paramfiledata['User']
passw = paramfiledata['Pass']
restversion = paramfiledata['RestVersion']

con=API(baseurl, user, passw, restversion)