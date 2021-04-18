import requests 

URL_CRACKMAPEXEC = 'http://crackmapexec:80/'

class crackmapexecModel():
    def __init__(self, scan_name, list_target, domain, username, password):
        self.scan_name = scan_name
        self.list_target = list_target
        self.domain = domain 
        self.username = username
        self.password = password
    
    def is_docker_alive(self):
        get_request = requests.get(URL_CRACKMAPEXEC)
        if get_request.status_code == 200:
            return {'isUp': True}

        return {'isUp': False}

    def start_crackmapexec(self):
        data = {
            'scan_name' : self.scan_name,
            "list_target" : self.list_target,
            "domain" : self.domain,
            'username' : self.username,
            'password' : self.password,
        }
        try : 
            response_post_request = requests.post(URL_CRACKMAPEXEC,json=data)
        except :
            return {'error':'Error during crackmapexec'}

        if response_post_request.status_code == 200:
            return response_post_request.json()

        return {'error':'status code isnot 200'}


