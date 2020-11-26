from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required , get_jwt_identity

from models.scan import ScanModel
from schema.scan import ScanSchema
from models.user import UserModel
from models.team import TeamModel

class NewScan(Resource):
    @jwt_required
    def post(self):
        errors = ScanSchema().validate(request.get_json())
        if errors:
            return {"message" : "Problem with Inputs" , "errors" : errors} , 400

        user = UserModel.find_by_id(get_jwt_identity())
        if(not(user)):
            return {'message': 'User not found'}, 400

        team = TeamModel.find_by_id(request.get_json()['team'])
        if(not(team)):
            return {'message':'Team not found'} , 400

        scan = request.get_json()
        try :
            scanId = ScanModel(scan['name'],scan['ip'],get_jwt_identity(),scan['team']).LaunchScript(user['server']['ip'],user['server']['password'])
        except:
            return {"message": "An error occurred during the scan."}, 500

        return {'message': "Success" , 'scanId': str(scanId)} , 201        

class Scan(Resource):
    @jwt_required                 
    def get(self, _idScan):
        scan = ScanModel.find_by_id(_idScan)
        if scan : 

            user = UserModel.find_by_id(scan['user'])
            if not(user): 
                return {'message': 'User not found'}, 400

            team = TeamModel.find_by_id(scan['team'])
            if not(team): 
                return {'message': 'Team not found'}, 400

            if TeamModel.is_in_team(get_jwt_identity(),team['admin'],team['users']):
                team = TeamModel(team['_id'],team['name'],team['admin'],team['users']).json()
                user = UserModel(user["surname"],user["name"],user["mail"],user["job"],user['server']['ip']).json()
                return ScanModel(scan['name'],scan['ip'],user,team).json_one_scan(scan['_id'],scan['date'],scan['nmap'],scan['metasploit']),200
            
            return {'message': 'Unauthorized'},401

        return {'message': 'Scan not found'}, 400

class Scans(Resource):
    @jwt_required 
    def get(self):
        scans = ScanModel.find_all()
        if scans: 
            arrayScan = [] 
            for scan in scans:
                user = UserModel.find_by_id(scan['user'])
                team = TeamModel.find_by_id(scan['team'])
                if team and user:
                    if TeamModel.is_in_team(get_jwt_identity(),team['admin'],team['users']) or str(user['_id']) == str(get_jwt_identity()):
                        user = {'surname': user['surname'],'name' : user['name']}
                        team = {'name':team['name']}
                        arrayScan.append(ScanModel(scan['name'],scan['ip'],user,team).json_several_scan(scan['_id'],scan['date'],scan['nmap']))
        
            return arrayScan , 200

        return {'message' : 'Any scan'} , 400


