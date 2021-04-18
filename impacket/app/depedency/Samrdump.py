from __future__ import division
from __future__ import print_function
import sys
import logging
import codecs
from argparse import Namespace

from datetime import datetime
from impacket.examples import logger
from impacket import version
from impacket.nt_errors import STATUS_MORE_ENTRIES
from impacket.dcerpc.v5 import transport, samr
from impacket.dcerpc.v5.rpcrt import DCERPCException

class ListUsersException(Exception):
    pass

class SAMRDump: 
    def __init__(self, username='', password='', domain='', hashes=None,
                 aesKey=None, doKerberos=False, kdcHost=None, port=445, csvOutput=False):

        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = aesKey
        self.__doKerberos = doKerberos
        self.__kdcHost = kdcHost
        self.__port = port
        self.__csvOutput = csvOutput

        if hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

    @staticmethod
    def getUnixTime(t):
        t -= 116444736000000000
        t /= 10000000
        return t

    def dump(self, remoteName, remoteHost):
        """Dumps the list of users and shares registered present at
        remoteName. remoteName is a valid host name or IP address.
        """

        entries = []

        stringbinding = r'ncacn_np:%s[\pipe\samr]' % remoteName
        logging.debug('StringBinding %s'%stringbinding)
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        rpctransport.set_dport(self.__port)
        rpctransport.setRemoteHost(remoteHost)

        if hasattr(rpctransport, 'set_credentials'):
            # This method exists only for selected protocol sequences.
            rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash,
                                         self.__nthash, self.__aesKey)
        rpctransport.set_kerberos(self.__doKerberos, self.__kdcHost)

        try:
            entries = self.__fetchList(rpctransport)
        except Exception as e:
            logging.critical(str(e))

        list_user = []

        for entry in entries:
            (username, uid, user) = entry
            pwdLastSet = (user['PasswordLastSet']['HighPart'] << 32) + user['PasswordLastSet']['LowPart']
            if pwdLastSet == 0:
                pwdLastSet = '<never>'
            else:
                pwdLastSet = str(datetime.fromtimestamp(self.getUnixTime(pwdLastSet)))

            if user['UserAccountControl'] & samr.USER_DONT_EXPIRE_PASSWORD:
                dontExpire = 'True'
            else:
                dontExpire = 'False'

            if user['UserAccountControl'] & samr.USER_ACCOUNT_DISABLED:
                accountDisabled = 'True'
            else:
                accountDisabled = 'False'

            list_user.append({
                'username':username,
                'uid' : uid,
                'fullname' : user['FullName'],
                'primary_group_id': user['PrimaryGroupId'],
                'bad_password_count' : user['BadPasswordCount'],
                'logon_count':user['LogonCount'],
                'password_last_set' : pwdLastSet,
                'is_expire':dontExpire,
                'is_disable':accountDisabled,
                'comment':user['UserComment']
            })

        return list_user
    


    def __fetchList(self, rpctransport):
        dce = rpctransport.get_dce_rpc()

        entries = []

        dce.connect()
        dce.bind(samr.MSRPC_UUID_SAMR)

        try:
            resp = samr.hSamrConnect(dce)
            serverHandle = resp['ServerHandle'] 

            resp = samr.hSamrEnumerateDomainsInSamServer(dce, serverHandle)
            domains = resp['Buffer']['Buffer']

            resp = samr.hSamrLookupDomainInSamServer(dce, serverHandle,domains[0]['Name'] )

            resp = samr.hSamrOpenDomain(dce, serverHandle = serverHandle, domainId = resp['DomainId'])
            domainHandle = resp['DomainHandle']

            status = STATUS_MORE_ENTRIES
            enumerationContext = 0
            while status == STATUS_MORE_ENTRIES:
                try:
                    resp = samr.hSamrEnumerateUsersInDomain(dce, domainHandle, enumerationContext = enumerationContext)
                except DCERPCException as e:
                    if str(e).find('STATUS_MORE_ENTRIES') < 0:
                        raise 
                    resp = e.get_packet()

                for user in resp['Buffer']['Buffer']:
                    r = samr.hSamrOpenUser(dce, domainHandle, samr.MAXIMUM_ALLOWED, user['RelativeId'])
                    info = samr.hSamrQueryInformationUser2(dce, r['UserHandle'],samr.USER_INFORMATION_CLASS.UserAllInformation)
                    entry = (user['Name'], user['RelativeId'], info['Buffer']['All'])
                    entries.append(entry)
                    samr.hSamrCloseHandle(dce, r['UserHandle'])

                enumerationContext = resp['EnumerationContext'] 
                status = resp['ErrorCode']

        except ListUsersException as e:
            logging.critical("Error listing users: %s" % e)

        dce.disconnect()

        return entries

def create_args_samrdump(domain, username, password, remote_name, target_ip, port):
    target = domain + "/"+username+':'+password+'@'+remote_name
    args = Namespace(
        aesKey=None, 
        csv=False, 
        dc_ip=None, 
        debug=False, 
        hashes=None, 
        k=False, 
        no_pass=False, 
        port=str(port), 
        target=str(target), 
        target_ip=target_ip, 
        ts=False
    )
    return args 

