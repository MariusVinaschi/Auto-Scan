from typing import Optional
import nmap3
import ipaddress
import socket
from multiprocessing import Pool , cpu_count

class PortScan:
    def __init__(self, name : str):
        self.name = name
        self.targets = []
        self.listResult = []

    ##### main Function ##### 
    def startNmap(self, listTargets : list):
        if type(listTargets) is not list:
            return False 

        self.setTargets(self.defineListTargets(listTargets))
        pool = Pool(processes = cpu_count()-1)
        for target in self.targets: 
            pool.apply_async(self.ScanHost, args = (target,), callback = self.addResult)
        
        pool.close()                
        pool.join()
        
        ScanResult = {}
        ScanResult['name'] = self.name        
        ScanResult['hosts'] = self.listResult

        return ScanResult    

    ##### Start Port Scan ###### 
    def ScanHost(self, host : str):
        nmap = nmap3.Nmap()
        
        dictResultHost = {}
        dictResultHost['IP'] = host 
        
        result = nmap.nmap_version_detection(host)

        if str(host) in result.keys(): 
            if 'hostname' in result[host].keys():
                dictResultHost['name'] = self.extractNameResult(result[host]['hostname'])
                
            if 'ports' in result[host].keys(): 
                dictResultHost['Ports'] = self.extractPortResult(result[host]['ports'])
            
            return dictResultHost

        result = nmap.nmap_version_detection(host,args='-Pn')

        if str(host) in result.keys():
            if 'hostname' in result[host].keys():
                dictResultHost['name'] = self.extractNameResult(result[host]['hostname'])
                
            if 'ports' in result[host].keys(): 
                dictResultHost['Ports'] = self.extractPortResult(result[host]['ports'])

            return dictResultHost

    ##### Save Result ##### 
    def extractNameResult(self, result : list): 
        if len(result) != 0:
            if 'name' in result[0].keys():
                return result[0]['name']
        return ''

    def extractPortResult(self, result : list): 
        arrayPort = []
        for Port in result:
            dictPort = {}
            dictPort['portid'] = Port['portid']
            if 'service' in Port:
                dictPort['service'] = Port['service']['name']
                if 'product' in Port['service']:
                    dictPort['product'] = Port['service']['product']
                if 'extrainfo' in Port['service']:
                    dictPort['extrainfo'] = Port['service']['extrainfo']

            arrayPort.append(dictPort)

        return arrayPort

    ##### Make a list with all the targets ##### 
    def defineListTargets(self, listTargets : list): 
        list = []
        for target in listTargets: 
            if PortScan.isValidIp(target) == False and PortScan.isRangeIp(target): 
                for host in self.NmapNoPortScan(target):
                    self.addTarget(host,list)
            else: 
                self.addTarget(target,list)
        
        return list

    ##### No Port Scan - Just to get all IP in Range IP ##### 
    def NmapNoPortScan(self, rangeIP : str): 
        result = nmap3.Nmap().nmap_list_scan(rangeIP)
        listHost = []
        for host in result.keys(): 
            if self.isValidIp(host) and result[host]['hostname'] != []:
                listHost.append(host)
        
        return listHost

    ##### Add Target ###### 
    def addTarget(self,target : str, listTarget : list): 
        if target not in listTarget:
            listTarget.append(target)

    ##### Validation ######

    ##### Valid hostname (google.com) return Boolean #####
    @classmethod
    def isValidHostname(cls, hostname : str ):
        try:
            socket.gethostbyname(hostname)
            return True 
        except socket.error:
            return False

    @classmethod
    def isValidIp(cls, hostIp : str):
        try: 
            ipaddress.ip_network(hostIp, strict=True)
            return True
        except ValueError:
            return False 

    @classmethod
    def isRangeIp(cls, hostIp : str):
        try:
            ipaddress.ip_network(hostIp, strict=False)
            return True
        except ValueError:
            return False 

    ##### setter ###### 
    def setTargets(self, listTargets : list):
        if type(listTargets) is list:
            self.targets = listTargets

    ##### addResult ###### 
    def addResult(self,result):
        self.listResult.append(result)