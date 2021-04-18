import requests
import os

URL_RESPONDER = 'http://'+str(os.environ['IP_RESPONDER'])+':80/'

class responderModel():
    def __init__(self, scan_name, list_target, interface, our_ip):
        self.scan_name = scan_name
        self.list_target = list_target
        self.interface = interface
        self.our_ip = our_ip

    def is_docker_alive(self):
        try: 
            get_request = requests.get(URL_RESPONDER)
            if get_request.status_code == 200:
                return {'isUp': True}

            return {'isUp': False}
        except: 
            return {'isUp': False}

    def start_responder(self):
        
        if self.interface == "ALL" and (self.our_ip == None or  self.our_ip == ''):
            return {'error':"You can't put ALL in interface and don't specify an IP"}

        data = {
            'scan_name' : self.scan_name,
            "list_target" : self.list_target,
            "interface":self.interface,
            "our_ip":self.our_ip
        }   

        try: 
            response_post_request = requests.post(URL_RESPONDER,json=data)         
        except: 
            return {'error':'Error during responder'}

        if response_post_request.status_code == 200:
            return response_post_request.json()

        return {'error':'Status code is not 200'}   