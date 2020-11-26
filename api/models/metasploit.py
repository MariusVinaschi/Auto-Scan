from pymetasploit3.msfrpc import MsfRpcClient

class Metasploit(): 
    def __init__(self, ip ,client ,openPort,dictModules):
        self.ip = ip
        self.client = client 
        self.openPort = openPort
        self.dictModules = dictModules

    def metasploitScript(self):
        resultMetasploit = []
        console_id = self.client.consoles.console().cid
        for port in self.openPort:
            if(self.checkPort(port['port'])):
                newPort = {}
                newPort['port'] = port['port']
                newPort['modules'] = self.launchPortModules(port['port'],console_id)
                resultMetasploit.append(newPort)

        return resultMetasploit

    def launchPortModules(self,port,console_id):
        resultModules = []
        for module in self.dictModules[port]['modules']:
            dict_module = {}
            nameModule = module['name']
            dict_module['name'] = nameModule
            exploit = self.client.modules.use('auxiliary',str(nameModule))
            self.setParameter(exploit,module['parameters'])
            output = self.client.consoles.console(console_id).run_module_with_output(exploit)                
            dict_module['results'] = self.extractResult(output)
            resultModules.append(dict_module)

        return resultModules

    def setParameter(self,exploit,arrayParameters): 
        for parameter in arrayParameters: 
            if(parameter['label'] == "RHOST" or parameter['label'] == "RHOSTS"):
                exploit[parameter['label']] = self.ip
            else:
                exploit[parameter['label']] = parameter['value']
            
    
    def extractResult(self , output): 
        arrayOutput = output.splitlines()
        for index,line in enumerate(arrayOutput):
            if("DisablePayloadHandler" in line):
                del arrayOutput[:index+1]
        
        del arrayOutput[-2:]

        return arrayOutput

    def checkPort(self, port): 
        if(port in self.dictModules):
            return True
        return False