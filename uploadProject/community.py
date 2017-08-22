#!/usr/bin/env python

import requests
import sys
import APIMethod as api
import logging
import Error as er
my_logger = logging.getLogger('Collibra')

class Community:

    def __init__(self,name='',rid='',parent='',p_rid='',desc='',uri=''):
        self.name=name
        self.parent=parent
        self.p_rid=p_rid
        self.desc=desc
        self.uri=uri
        self.rid=rid
        self.statusCode=0


    def postCommunity(self):

        endpoint = "community"
        prnt = self.parent.strip()
        if prnt:
            self.p_rid=Community.communityFind(prnt).rid
            if self.p_rid==1:
                my_logger.error("Error: %s parent community not found" % self.parent)
                self.p_rid =''
                return 1


        payload = {'name': self.name,'description' : self.desc,'parent':self.p_rid}

        try:
            j = api.API.postCall(endpoint, payload)
            my_logger.info('%s community is posted successfully' % self.name)
            return 0
        except er.CollibraPostException as e:
            my_logger.error("Exception Caught: "+ str(e.args))
            return 1



    @staticmethod
    def communityFind(name):

        """
        if self.name is None :
            return None

        if name is None :
            name = self.name

        endpoint = "community/find"


        payload = {'searchName': name}

        try:

            j = api.API.getCall(endpoint, payload)
            i = 0
            while (1):
                try:
                    commName = j['data']['communityReference'][i]['name']
                    if (commName == name):
                        self.uri=j['data']['communityReference'][i]['uri']
                        return j['data']['communityReference'][i]['resourceId']
                        break
                    else:
                        i = i + 1
                except IndexError:
                    my_logger.debug('%s Community not found' % name)
                    #raise er.CommunityNotFound("Exception while finding the community %s, no such community exist" % self.name)
                    return 1
        except er.CollibraGetException as e:
                    my_logger.error("Exception Caught: " + str(e.args))
                    return 1"""

        endpoint="community"

        payload = {'name': name}

        comm = Community()
        try:
            j=api.API.getCall(endpoint, payload)
            #return j['data']['parentReference']['name']
            comm.name = j['data']['name']
            comm.uri = j['data']['uri']
            comm.rid = j['data']['resourceId']
            #comm.parent = j['data']['parentReference']['name']
            #comm.p_rid=j['data']['parentReference']['resourceId']
            return comm

        except er.CollibraGetException as e:
            my_logger.error("Exception Caught: " + str(e.args))
            comm.statusCode=1
            return comm



    def getCommunityTerm(self,*term):


            endpoint = "community/%s/terms" % self.rid
            payload = {'community': self.rid,'searchSignifier' : term}
            listOfTerms = list()

            try:
                j = api.API.getCall(endpoint, payload)
                for iTerm in j['data']['attachment']:
                    trm = {'fileName': iTerm['fileName'], 'resourceId': iTerm['resourceId']}
                    listOfTerms.append(trm)
                return listOfTerms

            except er.CollibraGetException as e:
                my_logger.error("Exception Caught: " + str(e.args))

    def getCommunityAttachment(self):

            endpoint = "community/%s/attachments" % self.rid
            payload = {'baseResource': self.rid}
            listOfAttachment = list()

            try:
                j = api.API.getCall(endpoint, payload)
                for iAttchmnt in j['data']['attachment']:
                    att = {'fileName': iAttchmnt['fileName'], 'resourceId': iAttchmnt['resourceId']}
                    listOfAttachment.append(att)
                return listOfAttachment

            except er.CollibraGetException as e:
                my_logger.error("Exception Caught: " + str(e.args))



    def getCommunityParent(self):

        endpoint = "community/%s/parent" % self.rid
        parent = Community()

        payload = {'community': self.rid}
        try:
            j = api.API.getCall(endpoint, payload)
            parent.name = j['data']['name']
            parent.rid = j['data']['resourceId']
        except er.CollibraGetException as e:
            my_logger.error("Exception Caught: " + str(e.args))

        return parent

    def postCommunityParent(self, parent):

        try:
            p_rid = self.communityFind(parent)
        except er.CommunityNotFound as e:
            my_logger.error("Exception Caught: " + str(e.args))
            return 0

        endpoint = "community/%s/parent" % self.rid


        payload = {'community': self.rid, 'parent': p_rid}

        try:
            j = api.API.postCall(endpoint, payload)
            my_logger.info("%s community is successfully updated as child of %s community" % (self.name, parent))
            return j
        except er.CollibraPostException as e:
            my_logger.error("Exception Caught: " + str(e.args))



    def deleteCommunityParent(self):

        endpoint = "community/%s/parent" % self.rid


        payload = {'community': self.rid}

        try:
            j = api.API.deleteCall(endpoint, payload)
            return j
        except er.CollibraDelException as e:
            my_logger.error("Exception Caught: " + str(e.args))


    def getSubCommunity(self):

        Community.baseurl = "http://536918-app1.exusia.com:8080/dgc/rest"

        endpoint = "community/%s/sub-communities" % self.rid
        payload = {'community': self.rid}

        listOfSubComm = list()

        try:
            j = api.API.getCall(endpoint, payload)
            for iSubComm in j['data']['communityReference']:
                l_subcomm = {'name': iSubComm['name'], 'resourceId': iSubComm['resourceId']}
                listOfSubComm.append(l_subcomm)
            return listOfSubComm
        except er.CollibraPostException as e:
            my_logger.error("Exception Caught: " + str(e.args))


    def getCommunityVocab(self, vocab):

        Community.baseurl = "http://536918-app1.exusia.com:8080/dgc/rest"

        endpoint = "community/%s/vocabularies" % self.rid
        payload = {'community': self.rid, 'searchName': vocab}
        listOfVocab = list()

        try:
            j = api.API.getCall(endpoint, payload)
            for iVocab in j['data']['vocabularyReference']:
                l_vocab = {'name': iVocab['name'], 'resourceId': iVocab['resourceId']}
                listOfVocab.append(l_vocab)
            return listOfVocab
        except er.CollibraPostException as e:
            my_logger.error("Exception Caught: " + str(e.args))


    def postCommunityDesc(self, desc):

        endpoint = "community/%s/description" % self.rid

        payload = {'community': self.rid, 'description': desc}

        try:
            j = api.API.postCall(endpoint, payload)
            my_logger.info('%s community description is updated successfully' % self.name)
            return j
        except er.CollibraPostException as e:
            my_logger.error("Exception Caught: " + str(e.args))

    def updCommunity(self,name,desc=''):

        endpoint = "community/%s" % self.rid

        payload = {'community': self.rid, 'name': name,'description': desc}

        try:
            j = api.API.postCall(endpoint, payload)
            my_logger.info('%s community name and description is updated successfully' % self.name)
            return j
        except er.CollibraPostException as e:
            my_logger.error("Exception Caught: " + str(e.args))

    def getCommunityTask(self):

        endpoint = "community/%s/task" % self.rid


        payload = {'community': self.rid}
        try:
            j = api.API.getCall(endpoint, payload)
            return j
        except er.CollibraGetException as e:
            my_logger.error("Exception Caught: " + str(e.args))



    def deleteCommunityAsync(self,*name_list):
        final_list=list(name_list)+[self.name]
        try:
            rid_list = [self.communityFind(x) for x in final_list ]
        except er.CommunityNotFound as e:
            my_logger.error("Exception Caught: " + str(e.args))
            return 0

        endpoint = "community/remove/async"


        payload = {'resource': rid_list}
        try:
            j = api.API.deleteCall(endpoint, payload)
            my_logger.info(','.join(final_list), "community is deleted sussessfully")
        except er.CollibraDelException as e:
            my_logger.error("Exception Caught: " + str(e.args))







