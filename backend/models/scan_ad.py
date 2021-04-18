from bson.objectid import ObjectId
import datetime
import re 

from models.nmap_ad import nmapModel
from models.responder import responderModel
from models.john import johnModel
from models.crackmapexec import crackmapexecModel
from models.impacket import impacketModel
from models.smbmap import smbmapModel

REGEX_DOMAIN_AND_USERNAME = r'^([\w-]{1,})\\([\w-]{1,})$'

class ScanAdModel():
    def __init__(self, scan_name, list_target, user, team):
        self.scan_name = scan_name 
        self.list_target = list_target
        self.user = user 
        self.team = team 

    def start_scan_ad(self, interface, our_ip):
        
        result_scan_ad = {}

        result_scan_ad = self.init_result_scan_ad(result_scan_ad)

        # Check if Docker Nmap up 
        nmap = nmapModel(self.scan_name,self.list_target)
        if nmap.is_docker_alive()['isUp'] == False: 
            return {"error": 'Error with the Nmap docker'}

        # Launch Nmap 
        result_nmap = nmap.start_nmap()
        if 'error' in result_nmap:
            return {'error': result_nmap['error']}

        # put the result in the dict
        result_scan_ad['hosts'] = result_nmap['hosts']
        result_scan_ad = self.init_domain_information(result_scan_ad)   

        # Check if Docker Responder up 
        responder = responderModel(self.scan_name, self.list_target, interface, our_ip)
        if responder.is_docker_alive()['isUp'] == False: 
            return {'error': 'Error with the responder docker'}

        # Launch Responder 
        result_responder = responder.start_responder()
        if 'error' in result_responder:
            return {'error': result_responder['error']}

        if len(result_responder['result']) == 0: 
            return {'error': 'No hash NTLMv2 need to be crack'}

        result_scan_ad = self.set_domain_name_if_not_in_nmap(result_responder,result_scan_ad)

        if 'name' not in result_scan_ad['domain']:
            return {'error':"Can't find the domain name"}

        # Check if john the ripper is up 
        johntheripper = johnModel(self.scan_name)
        if johntheripper.is_docker_alive()['isUp'] == False: 
            return {'error':'Error with john docker'}

        # break all the hash find with responder  
        list_credentials = []
        for responder_hash in result_responder['result']:
            username = self.find_username(responder_hash['user'])
            result_john = johntheripper.start_john_ntlmv2(username, result_scan_ad['domain']['name'], responder_hash['fullhash'])
            if "error" not in result_john and result_john['password'] != '' : 
                list_credentials.append({
                    'ip' : responder_hash['client'],
                    'domain' : result_john['domain'],
                    'username': result_john['username'],
                    'password': result_john['password']
                })

        # If no creds stop the scans
        if len(list_credentials) == 0:
            return result_scan_ad

        result_scan_ad['credentials'] = list_credentials

        # Need to make that with several credentials 

        credential = list_credentials[0]
        
        # CrackMapExec # 
        crackmapexec = crackmapexecModel(self.scan_name,self.list_target,credential['domain'],credential['username'],credential['password'])
        if crackmapexec.is_docker_alive()['isUp'] == True: 
            result_crackmapexec = crackmapexec.start_crackmapexec()
            result_scan_ad = self.save_crackmapexec_result(result_crackmapexec, result_scan_ad)
        
        # Impacket # 
        impacket = impacketModel(self.scan_name, result_scan_ad['domain']['name'],result_scan_ad['domain']['domain_controler_ip'],self.list_target,credential['username'],credential['password'])
        if impacket.is_docker_alive()['isUp'] == True: 
            result_GetAdUsers = impacket.start_GetAdUsers()
            result_scan_ad = self.save_getAduser(result_GetAdUsers,result_scan_ad)

            result_GetUserSPNs = impacket.start_GetUserSPNs()
            result_scan_ad = self.save_getUserSPNs(result_GetUserSPNs,result_scan_ad)

            for index,host in enumerate(result_scan_ad['hosts']):
                result_Samrdump = impacket.start_Samrdump(host['IP'])
                result_lookupsid = impacket.start_lookupsid(host['IP'])
                result_scan_ad = self.save_lookupsid_and_samrdump(index, result_Samrdump,result_lookupsid,result_scan_ad)

        # SMBMAP # 
        smbmap = smbmapModel(self.scan_name,self.list_target,credential['username'],credential['password'],credential['domain'])
        if smbmap.is_docker_alive()['isUp'] == True: 
            result_smbmap = smbmap.start_smbmap()
            result_scan_ad = self.save_smbmap_result(result_smbmap,result_scan_ad)

        return result_scan_ad


    def add_db(self, hosts, domain, credentials):
        from app import mongo
        ScanId = mongo.db.ScansAd.insert_one(
            {
                "name" : self.scan_name,
                'list_target': self.list_target,
                "user" : ObjectId(self.user),
                "team" : ObjectId(self.team),
                "date" : datetime.datetime.utcnow(),
                'hosts' : hosts,  
                'domain' : domain, 
                'credentials': credentials 
            } 
        ).inserted_id
        return ScanId

    ##### Save in Dict ##### 

    def init_result_scan_ad(self,result_scan_ad):
        result_scan_ad['scan_name'] = self.scan_name
        return result_scan_ad

    def init_domain_information(self,result_scan_ad):
        index_domain_controler = None
        for index, host in enumerate(result_scan_ad['hosts']):
            list_port_number = []
            for port in host['Ports']:
                list_port_number.append(port['portid'])

            if '88' in list_port_number and '389' in list_port_number: 
                index_domain_controler = index
                break
        
        if index_domain_controler == None : 
            return {'error': "No domain controler"}

        result_scan_ad['hosts'][index_domain_controler]['domain_controller'] = True
        result_scan_ad['domain'] = {}
        result_scan_ad['domain']['domain_controler_ip'] = result_scan_ad['hosts'][index_domain_controler]['IP']
        result_scan_ad['domain']['domain_controler_name'] = result_scan_ad['hosts'][index_domain_controler]['name']
        domain = self.find_ad_name(result_scan_ad['hosts'][index_domain_controler])
        if domain is not None: 
            result_scan_ad['domain']['name'] = domain

        return result_scan_ad

    def find_ad_name(self,dict_domain_controler):
        list_port_ad = ['389','636','3268']
        for port in dict_domain_controler['Ports']:
            if port['portid'] in list_port_ad and 'extrainfo' in port:
                if 'Domain' in  port['extrainfo']: 
                    regex_domain = r'Domain:\s([\w-]{1,}).'
                    domain = re.findall(regex_domain,port['extrainfo'])
                    if len(domain) !=0 :  
                        return domain[0]

    def set_domain_name_if_not_in_nmap(self,result_responder,result_scan_ad):
        if 'name' not in result_scan_ad['domain']:
            list_match_regex = re.findall(REGEX_DOMAIN_AND_USERNAME,result_responder['result'][0]['user'])
            if len(list_match_regex)==1:  
                result_scan_ad['domain']['name'] = list_match_regex[0][0]

        return result_scan_ad

    def find_username(self,responder_username):
        list_match_regex = re.findall(REGEX_DOMAIN_AND_USERNAME,responder_username)
        username = ""
        if len(list_match_regex)==1:  
            username = list_match_regex[0][1]

        return username

    def save_crackmapexec_result(self, result_crackmapexec,result_scan_ad):    
        if len(result_crackmapexec['groups']) != 0:
            list_dict_group = []
            for group in result_crackmapexec['groups']:
                dict_group = { 
                    'name': group['name']
                }
                list_dict_group.append(dict_group)

            result_scan_ad['domain']['groups'] = list_dict_group

        if len(result_crackmapexec['users']) != 0:
            list_dict_user = []
            for user in result_crackmapexec['users']:
                dict_user = { 
                    'username': user['username'],
                    'password': user['password']
                }
                list_dict_user.append(dict_user)

            result_scan_ad['domain']['users'] = list_dict_user

        return result_scan_ad
                    
    def save_smbmap_result(self,result_smbmap,result_scan_ad):
        for index,host in enumerate(result_scan_ad['hosts']):
            f = list(filter(lambda share: share['host'] == host['IP'], result_smbmap['hosts']))
            if len(f) != 0: 
                result_scan_ad['hosts'][index]['shares'] = f[0]['shares']

        return result_scan_ad

    def save_getAduser(self,result_GetAdUsers,result_scan_ad):
        for index,user in enumerate(result_scan_ad['domain']['users']):
            f = list(filter(lambda u: u['username'] == user['username'], result_GetAdUsers['list_user']))
            if len(f) != 0: 
                for key,value in f[0].items():
                    if key not in user.keys():
                        result_scan_ad['domain']['users'][index][str(key)] = value
                    else:
                        if result_scan_ad['domain']['users'][index][str(key)] == '':
                            result_scan_ad['domain']['users'][str(key)] = value

        return result_scan_ad

    def save_getUserSPNs(self, result_GetUserSPNs,result_scan_ad):
        result_scan_ad['domain']['services'] = result_GetUserSPNs['list_services']
        return result_scan_ad

    def save_lookupsid_and_samrdump(self, index_result_scan_ad, result_Samrdump,result_lookupsid,result_scan_ad):
        if len(result_Samrdump['list_user']) !=0: 
            result_scan_ad['hosts'][index_result_scan_ad]['users'] = result_Samrdump['list_user']
        else : 
            result_scan_ad['hosts'][index_result_scan_ad]['users'] = result_lookupsid['list_user']

        return result_scan_ad

    def json_one_scan(self, _id, date, hosts, domain, credentials):
        return {
            'id' : str(_id),
            "name" : self.scan_name,
            'list_target': self.list_target,
            "user" : self.user,
            "team" : self.team,
            "date" : str(date),
            'hosts' : hosts,  
            'domain' : domain, 
            'credentials': credentials
        }

    def json_several_scan(self, _id, date, domain):
        return {
            'id' : str(_id),
            "name" : self.scan_name,
            "date" : str(date), 
            "list_target" : self.list_target,
            "user" : self.user,
            "team" : self.team,
            "domain" : domain,
        }

    @classmethod
    def find_by_id(cls, _idScan):
        from app import mongo 
        return mongo.db.ScansAd.find_one({'_id': ObjectId(_idScan)})
    
    @classmethod 
    def find_all(cls): 
        from app import mongo
        return mongo.db.ScansAd.find()
