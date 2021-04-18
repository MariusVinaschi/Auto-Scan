import os 

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required , get_jwt_identity

from models.user import UserModel
from models.team import TeamModel
from models.scan_ad import ScanAdModel

from schema.scan_ad import ScanADSchema

class NewScanAd(Resource):
    @jwt_required
    def post(self):
        errors = ScanADSchema().validate(request.get_json())
        if errors:
            return {"message":"Problem with Inputs","errors":errors},400

        # check user 
        user = UserModel.find_by_id(get_jwt_identity())
        if(not(user)):
            return {'message': 'User not found'}, 400

        # check team 
        team = TeamModel.find_by_id(request.get_json()['team'])
        if(not(team)):
            return {'message':'Team not found'} , 400

        scanAdInput = request.get_json()
        newAdScan = ScanAdModel(scanAdInput['scan_name'],scanAdInput['list_target'],get_jwt_identity(),scanAdInput['team'])
        try: 
            dict_result_scan = newAdScan.start_scan_ad('ALL',str(os.environ['IP_RESPONDER']))
        except:
            return {"message":'An error occurred during the scan'},500

        if 'error' in dict_result_scan:
            return {'error':dict_result_scan['error']}, 400

        scanId = newAdScan.add_db(dict_result_scan['hosts'], dict_result_scan['domain'], dict_result_scan['credentials'])
        return {'message': "Success" , 'scanId': str(scanId)} , 201 

        
class ScanAd(Resource):
    @jwt_required 
    def get(self,_idScan):
        scan = ScanAdModel.find_by_id(_idScan)
        if scan: 
            user = UserModel.find_by_id(scan['user'])
            if not(user): 
                return {'message': 'User not found'}, 400

            team = TeamModel.find_by_id(scan['team'])
            if not(team): 
                return {'message': 'Team not found'}, 400

            if TeamModel.is_in_team(get_jwt_identity(),team['admin'],team['users']):
                team = TeamModel(team['_id'],team['name'],team['admin'],team['users']).json()
                user = UserModel(user["surname"],user["name"],user["mail"],user["job"],user['server']['ip']).json()
                return ScanAdModel(scan['name'],scan['list_target'],user,team).json_one_scan(_idScan,scan['date'],scan['hosts'],scan['domain'],scan['credentials']),200
            
            return {'message': 'Unauthorized'},401

        return {'message': 'Scan not found'}, 400
            

class ScansAd(Resource):
    @jwt_required
    def get(self): 
        scansAd = ScanAdModel.find_all()
        if scansAd:
            arrayScansAd = []
            for scanAd in scansAd: 
                user = UserModel.find_by_id(scanAd['user'])
                team = TeamModel.find_by_id(scanAd['team'])
                if team and user: 
                    if TeamModel.is_in_team(get_jwt_identity(),team['admin'],team['users']) or str(user['_id']) == str(get_jwt_identity()):
                        user = {'surname': user['surname'],'name' : user['name']}
                        team = {'name':team['name']}
                        arrayScansAd.append(ScanAdModel(scanAd['name'],scanAd['list_target'],user,team).json_several_scan(scanAd['_id'],scanAd['date'],scanAd['domain']))
            
            return arrayScansAd , 200

        return {'message' : 'Any scan'} , 400