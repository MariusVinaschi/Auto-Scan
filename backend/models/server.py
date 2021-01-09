from pymetasploit3.msfrpc import MsfRpcClient

class ServerModel():
    def __init__(self, ip , password):
        self.ip = ip
        self.password = password

    def Connect(self): 
        return MsfRpcClient(self.password,server=self.ip,ssl=True,port=55553)

    def check_Connect(self,Client):
        if(not(Client.modules.exploits)):
            return False
        return True


        