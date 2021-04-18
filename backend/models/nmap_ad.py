import requests

URL_NMAP = 'http://nmap:80/'

class nmapModel():
    def __init__(self, scan_name, list_target):
        self.scan_name = scan_name
        self.list_target = list_target

    def is_docker_alive(self):
        try: 
            get_request = requests.get(URL_NMAP)
            if get_request.status_code == 200:
                return {'isUp': True}

            return {'isUp': False}
        except :
            return {'isUp': False}

    def start_nmap(self):
        data = {
            'scan_name' : self.scan_name,
            'list_target' : self.list_target,
        }
        try : 
            response_post_request = requests.post(URL_NMAP,json=data)
        except :
            return {'error':'Error during nmap'}

        if response_post_request.status_code != 200 : 
            return {'error':'Bad Status code'}

        if response_post_request.json()['result'] == False:
            return {'error':'Error during nmap'}
        
        data_nmap = response_post_request.json()
        if 'hosts' not in data_nmap:
            return {'error':'No key hosts in the result of Nmap'}

        return data_nmap
  