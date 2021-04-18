#!/usr/bin/env python
# SECUREAUTH LABS. Copyright 2018 SecureAuth Corporation. All rights reserved.
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# DCE/RPC lookup sid brute forcer example
#
# Author:
#  Alberto Solino (@agsolino)
#
# Reference for:
#  DCE/RPC [MS-LSAT]
from __future__ import division
from __future__ import print_function
import logging

from argparse import Namespace
from impacket.examples import logger
from impacket import version
from impacket.dcerpc.v5 import transport, lsat, lsad
from impacket.dcerpc.v5.samr import SID_NAME_USE
from impacket.dcerpc.v5.dtypes import MAXIMUM_ALLOWED
from impacket.dcerpc.v5.rpcrt import DCERPCException


class LSALookupSid:
    KNOWN_PROTOCOLS = {
        139: {'bindstr': r'ncacn_np:%s[\pipe\lsarpc]', 'set_host': True},
        445: {'bindstr': r'ncacn_np:%s[\pipe\lsarpc]', 'set_host': True},
    }

    def __init__(self, username='', password='', domain='', port = None,
                 hashes = None, domain_sids = False, maxRid=4000):

        self.__username = username
        self.__password = password
        self.__port = port
        self.__maxRid = int(maxRid)
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__domain_sids = domain_sids
        if hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

    def dump(self, remoteName, remoteHost):
        list_user = []

        stringbinding = self.KNOWN_PROTOCOLS[self.__port]['bindstr'] % remoteName
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        rpctransport.set_dport(self.__port)

        if self.KNOWN_PROTOCOLS[self.__port]['set_host']:
            rpctransport.setRemoteHost(remoteHost)

        if hasattr(rpctransport, 'set_credentials'):
            # This method exists only for selected protocol sequences.
            rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)

        try:
            list_user = self.__bruteForce(rpctransport, self.__maxRid)
        except Exception as e:
            if logging.getLogger().level == logging.DEBUG:
                import traceback
                traceback.print_exc()
            logging.critical(str(e))
            raise

        return list_user

    def __bruteForce(self, rpctransport, maxRid):
        dce = rpctransport.get_dce_rpc()
        list_user = []
        dce.connect()

        dce.bind(lsat.MSRPC_UUID_LSAT)
        
        resp = lsad.hLsarOpenPolicy2(dce, MAXIMUM_ALLOWED | lsat.POLICY_LOOKUP_NAMES)
        policyHandle = resp['PolicyHandle']

        if self.__domain_sids: # get the Domain SID
            resp = lsad.hLsarQueryInformationPolicy2(dce, policyHandle, lsad.POLICY_INFORMATION_CLASS.PolicyPrimaryDomainInformation)
            domainSid =  resp['PolicyInformation']['PolicyPrimaryDomainInfo']['Sid'].formatCanonical()
        else: # Get the target host SID
            resp = lsad.hLsarQueryInformationPolicy2(dce, policyHandle, lsad.POLICY_INFORMATION_CLASS.PolicyAccountDomainInformation)
            domainSid = resp['PolicyInformation']['PolicyAccountDomainInfo']['DomainSid'].formatCanonical()

        soFar = 0
        SIMULTANEOUS = 1000
        for j in range(maxRid//SIMULTANEOUS+1):
            if (maxRid - soFar) // SIMULTANEOUS == 0:
                sidsToCheck = (maxRid - soFar) % SIMULTANEOUS
            else: 
                sidsToCheck = SIMULTANEOUS
 
            if sidsToCheck == 0:
                break

            sids = list()
            for i in range(soFar, soFar+sidsToCheck):
                sids.append(domainSid + '-%d' % i)
            try:
                lsat.hLsarLookupSids(dce, policyHandle, sids,lsat.LSAP_LOOKUP_LEVEL.LsapLookupWksta)
            except DCERPCException as e:
                if str(e).find('STATUS_NONE_MAPPED') >= 0:
                    soFar += SIMULTANEOUS
                    continue
                elif str(e).find('STATUS_SOME_NOT_MAPPED') >= 0:
                    resp = e.get_packet()
                else: 
                    raise

            

            for n, item in enumerate(resp['TranslatedNames']['Names']):
                if item['Use'] != SID_NAME_USE.SidTypeUnknown:

                    sid = soFar + n
                    domain = resp['ReferencedDomains']['Domains'][item['DomainIndex']]['Name']
                    username = str(resp['ReferencedDomains']['Domains'][item['DomainIndex']]['Name'])+'/'+item["Name"]
                    sid_use = SID_NAME_USE.enumItems(item['Use']).name

                    list_user.append({
                        'sid': sid,
                        'domain':domain,
                        'username':username,
                        'sid_use':sid_use
                    })  
                    
            soFar += SIMULTANEOUS

        dce.disconnect()

        return list_user


def create_args_lookupsid(domain,username,password,remoteName,ip_target):
    target = domain + "/"+username+':'+password+'@'+remoteName
    args = Namespace(
        target=str(target), 
        port='445', 
        maxRid='4000', 
        domain_sids=False, 
        hashes=None, 
        no_pass=False, 
        target_ip=ip_target, 
        ts=False
    )
    return args 

