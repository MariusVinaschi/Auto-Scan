#!/usr/bin/env python
# SECUREAUTH LABS. Copyright 2018 SecureAuth Corporation. All rights reserved.
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# Author:
#  Alberto Solino (@agsolino)
#
# Description:
#     This script will gather data about the domain's users and their corresponding email addresses. It will also
#     include some extra information about last logon and last password set attributes.
#     You can enable or disable the the attributes shown in the final table by changing the values in line 184 and
#     headers in line 190.
#     If no entries are returned that means users don't have email addresses specified. If so, you can use the
#     -all-users parameter.
#
# Reference for:
#     LDAP
#
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from argparse import Namespace
import logging
import sys
from datetime import datetime

from impacket import version
from impacket.dcerpc.v5.samr import UF_ACCOUNTDISABLE
from impacket.examples import logger
from impacket.ldap import ldap, ldapasn1
from impacket.smbconnection import SMBConnection


class GetADUsers:
    def __init__(self, username, password, domain, cmdLineOptions):
        self.options = cmdLineOptions
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = cmdLineOptions.aesKey
        self.__doKerberos = cmdLineOptions.k
        self.__target = None
        self.__kdcHost = cmdLineOptions.dc_ip
        self.__requestUser = cmdLineOptions.user
        self.__all = cmdLineOptions.all
        if cmdLineOptions.hashes is not None:
            self.__lmhash, self.__nthash = cmdLineOptions.hashes.split(':')

        # Create the baseDN
        domainParts = self.__domain.split('.')
        self.baseDN = ''
        for i in domainParts:
            self.baseDN += 'dc=%s,' % i
        # Remove last ','
        self.baseDN = self.baseDN[:-1]

        # Let's calculate the header and format
        self.__header = ["Name", "Email", "PasswordLastSet", "LastLogon"]
        # Since we won't process all rows at once, this will be fixed lengths
        self.__colLen = [20, 30, 19, 19]
        self.__outputFormat = ' '.join(['{%d:%ds} ' % (num, width) for num, width in enumerate(self.__colLen)])

    def getMachineName(self):
        if self.__kdcHost is not None:
            s = SMBConnection(self.__kdcHost, self.__kdcHost)
        else:
            s = SMBConnection(self.__domain, self.__domain)
        try:
            s.login('', '')
        except Exception:
            if s.getServerName() == '':
                raise Exception('Error while anonymous logging into %s' % self.__domain)
        else:
            s.logoff()
        return s.getServerName()

    @staticmethod
    def getUnixTime(t):
        t -= 116444736000000000
        t /= 10000000
        return t

    def processRecord(self, item):
        if isinstance(item, ldapasn1.SearchResultEntry) is not True:
            return
        sAMAccountName = ''
        pwdLastSet = ''
        mail = ''
        lastLogon = 'N/A'
        try:
            for attribute in item['attributes']:
                if str(attribute['type']) == 'sAMAccountName':
                    if attribute['vals'][0].asOctets().decode('utf-8').endswith('$') is False:
                        # User Account
                        sAMAccountName = attribute['vals'][0].asOctets().decode('utf-8')
                elif str(attribute['type']) == 'pwdLastSet':
                    if str(attribute['vals'][0]) == '0':
                        pwdLastSet = '<never>'
                    else:
                        pwdLastSet = str(datetime.fromtimestamp(self.getUnixTime(int(str(attribute['vals'][0])))))
                elif str(attribute['type']) == 'lastLogon':
                    if str(attribute['vals'][0]) == '0':
                        lastLogon = '<never>'
                    else:
                        lastLogon = str(datetime.fromtimestamp(self.getUnixTime(int(str(attribute['vals'][0])))))
                elif str(attribute['type']) == 'mail':
                    mail = str(attribute['vals'][0])

            return {
                'username': sAMAccountName,
                'mail': mail,
                'password_last_set':pwdLastSet,
                'last_logon':lastLogon
            }

        except Exception as e:
            logging.debug("Exception", exc_info=True)
            logging.error('Skipping item, cannot process due to error %s' % str(e))
            return None

    def run(self):
        if self.__doKerberos:
            self.__target = self.getMachineName()
        else:
            if self.__kdcHost is not None:
                self.__target = self.__kdcHost
            else:
                self.__target = self.__domain

        # Connect to LDAP
        try:
            ldapConnection = ldap.LDAPConnection('ldap://%s'%self.__target, self.baseDN, self.__kdcHost)
            if self.__doKerberos is not True:
                ldapConnection.login(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)
            else:
                ldapConnection.kerberosLogin(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash,
                                             self.__aesKey, kdcHost=self.__kdcHost)
        except ldap.LDAPSessionError as e:
            if str(e).find('strongerAuthRequired') >= 0:
                # We need to try SSL
                ldapConnection = ldap.LDAPConnection('ldaps://%s' % self.__target, self.baseDN, self.__kdcHost)
                if self.__doKerberos is not True:
                    ldapConnection.login(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)
                else:
                    ldapConnection.kerberosLogin(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash,
                                                 self.__aesKey, kdcHost=self.__kdcHost)
            else:
                raise

        # Building the search filter
        if self.__all:
            searchFilter = "(&(sAMAccountName=*)(objectCategory=user)"
        else:
            searchFilter = "(&(sAMAccountName=*)(mail=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=%d))" % UF_ACCOUNTDISABLE

        if self.__requestUser is not None:
            searchFilter += '(sAMAccountName:=%s))' % self.__requestUser
        else:
            searchFilter += ')'

        try:
            logging.debug('Search Filter=%s' % searchFilter)
            sc = ldap.SimplePagedResultsControl(size=100)
            items = ldapConnection.search(searchFilter=searchFilter,
                                  attributes=['sAMAccountName', 'pwdLastSet', 'mail', 'lastLogon'],
                                  sizeLimit=0, searchControls = [sc])
        except ldap.LDAPSearchError:
                raise
        ldapConnection.close()

        list_user = []
        for item in items:
            user = self.processRecord(item)
            if user is not None:
                list_user.append(user)

        return list_user

def create_args_getadusers(dc_ip,domain,username,password,all):
    target = domain + "/"+username+':'+password
    args = Namespace(
        target=str(target), 
        dc_ip=str(dc_ip), 
        all=bool(all), 
        aesKey=None, 
        debug=False, 
        hashes=None, 
        k=False, 
        no_pass=False, 
        ts=False, 
        user=None
    )
    return args 

