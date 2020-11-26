from models.server import ServerModel
from models.metasploit import Metasploit
from models.nmap import Nmap
from models.modules import ModulesModel
from bson.objectid import ObjectId

import datetime


class ScanModel():
    def __init__(self, name, ip, user, team):
        self.name = name
        self.ip = ip
        self.user = user
        self.team = team


    def LaunchScript(self, ipMsfrpcd, passwordMsfrpcd):
        Client = ServerModel(ipMsfrpcd,passwordMsfrpcd).Connect()
        resultNmap = Nmap(self.ip).startNmap()
        modules = ModulesModel.find_modules_name('Basic_Scan')
        if modules: 
            dictModules = modules['ports']
            resultMetasploit = Metasploit(self.ip,Client,resultNmap,dictModules).metasploitScript()
            return self.add_db(resultNmap,resultMetasploit)

    def add_db(self , resultNmap, resultMetasploit):
        from app import mongo
        ScanId = mongo.db.Scans.insert_one(
            {
                "name" : self.name,
                "ip" : self.ip, 
                "user" : ObjectId(self.user),
                "team" : ObjectId(self.team),
                "date" : datetime.datetime.utcnow(),
                "nmap" : resultNmap,
                "metasploit" : resultMetasploit
            }
        ).inserted_id
        return ScanId

    def json_one_scan(self, _id, date, resultNmap, resultMetasploit):
        return {
            "id" : str(_id),
            "name":self.name,
            "ip" : self.ip,
            "user" : self.user,
            "team" : self.team,
            "date" : str(date),
            "nmap" : resultNmap,
            "metasploit" : resultMetasploit
        }

    def json_several_scan(self, _id, date, resultNmap):
        return {
            "id" : str(_id),
            "name":self.name,
            "ip" : self.ip,
            "user" : self.user,
            "team" : self.team,
            "date" : str(date),
            "nmap" : resultNmap,
        }

    @classmethod
    def find_by_id(cls, _idScan):
        from app import mongo 
        return mongo.db.Scans.find_one({'_id': ObjectId(_idScan)})
    
    @classmethod 
    def find_all(cls): 
        from app import mongo
        return mongo.db.Scans.find()

    

