import requests

URL_JOHN = 'http://john:80/'

class johnModel():
    def __init__(self, scan_name):
        self.scan_name = scan_name

    def is_docker_alive(self):
        try : 
            get_request = requests.get(URL_JOHN)
            if get_request.status_code == 200:
                return {'isUp': True}
            
            return {'isUp': False}
        except  :
            return {'isUp': False}

    def start_john_ntlmv2(self, username, domain, hash): 
        url_john_ntlmv2 = URL_JOHN + 'ntlmv2'
        data = {
            "username" : username,
            "domain" : domain,
            "hash" : hash
        }

        try : 
            response_post_request = requests.post(url_john_ntlmv2,json=data)
        except: 
            return {'error':'Error during john'}

        if response_post_request.status_code == 200:
                return response_post_request.json()

        return {'error':'Status code isnot 200'}