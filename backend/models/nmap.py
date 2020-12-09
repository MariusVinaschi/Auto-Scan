import nmap3

class Nmap(): 
    def __init__(self , ip):
        self.ip = ip

    def startNmap(self): 
        result = nmap3.Nmap().nmap_version_detection(self.ip)
        return self.saveNmapResult(result)   

    def saveNmapResult(self,result): 
        arrayPort = []
        for Port in result:
            dictPort = {}
            dictPort['port'] = Port['port']
            if('service' in Port):
                dictPort['service'] = Port['service']['name']
                # dictPort['product'] = Port['service']['product']

            arrayPort.append(dictPort)
        return arrayPort