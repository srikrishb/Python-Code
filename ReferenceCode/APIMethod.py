import requests
import logging
import Collibra.Error as ER



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


    def postCall(args, payload):
        url = "%s/%s/%s" % (con.baseurl, con.restversion, args)
        r = requests.post(url, auth=(con.useName, con.password), data=payload)
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

con=API('http://536918-app1.exusia.com:8080/dgc/rest','Admin','admin','1.0')