import requests

URL_IMPACKET = 'http://impacket:80/'

class impacketModel():
    def __init__(self,scan_name, domain, domain_controler_ip, list_target, username, password):
        self.scan_name = scan_name
        self.domain = domain 
        self.domain_controler_ip = domain_controler_ip
        self.list_target = list_target
        self.username = username
        self.password = password 

    def is_docker_alive(self):
        get_request = requests.get(URL_IMPACKET)
        dict_result = get_request.json()

        if 'Message' in dict_result:
            return {'isUp': True}

        return {'isUp': False}

    # scan_name : str target : str list_user : Optional[List] = []
    # Only dc
    def start_GetAdUsers(self):
        url_GetAdUsers = URL_IMPACKET + 'getadusers'
        data = {
            'scan_name' : self.scan_name,
            'domain' : self.domain,
            'domain_controler_ip' : self.domain_controler_ip,
            'username' : self.username,
            'password' : self.password
        }
        return self.request_post_impacket(url_GetAdUsers,data,'getadusers')

    # scan_name : str target : str list_user : Optional[List] = []
    # Only dc
    def start_GetUserSPNs(self):
        url_GetUserSPNs = URL_IMPACKET + 'getuserspns'
        data = {
            'scan_name' : self.scan_name,
            'domain' : self.domain,
            'domain_controler_ip' : self.domain_controler_ip,
            'username' : self.username,
            'password' : self.password
        }
        return self.request_post_impacket(url_GetUserSPNs,data,'getuserspns')

    # scan_name : str target : str list_user : Optional[List] = []
    def start_lookupsid(self, target_ip):
        url_lookupsid = URL_IMPACKET + 'lsalookupsid'
        data = {
            'scan_name' : self.scan_name,
            'domain' : self.domain,
            'domain_controler_ip' : self.domain_controler_ip,
            'username' : self.username,
            'password' : self.password,
            'target_ip': str(target_ip)
        }
        return self.request_post_impacket(url_lookupsid,data,'lookupsid')

    # scan_name : str target : str list_user : Optional[List] = []
    def start_Samrdump(self,target_ip):
        url_samrdump = URL_IMPACKET + 'samrdump'
        data = {
            'scan_name' : self.scan_name,
            'domain' : self.domain,
            'domain_controler_ip' : self.domain_controler_ip,
            'username' : self.username,
            'password' : self.password,
            'target_ip': str(target_ip)
        }
        return self.request_post_impacket(url_samrdump,data,'samrdump')

    def request_post_impacket(self,url,data,tool_name):
        try: 
            response_post_request = requests.post(url,json=data)
        except:
            return {'error':'Error during ' +str(tool_name)}
        
        if response_post_request.status_code == 200:
            return response_post_request.json()

        return {'error':'bad status code in this tool : ' +str(tool_name)}



