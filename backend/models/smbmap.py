import requests

URL_SMBMAP = 'http://smbmap:80/'

class smbmapModel():
    def __init__(self,scan_name, list_target, username, password, domain):
        self.scan_name = scan_name
        self.list_target = list_target
        self.username = username
        self.password = password 
        self.domain = domain 

    def is_docker_alive(self):
        get_request = requests.get(URL_SMBMAP)
        if get_request.status_code == 200:
            return {'isUp': True}

        return {'isUp': False}


    def start_smbmap(self):
        data = {
            'scan_name' : self.scan_name,
            "list_target" : self.list_target,
            "domain" : self.domain,
            'username' : self.username,
            'password' : self.password,
        }
        try : 
            response_post_request = requests.post(URL_SMBMAP,json=data)
        except:
            return {'error':'Error during smbmap'}
        
        if response_post_request.status_code == 200:
            return response_post_request.json()

        return {'error':'Error in the status code'}





