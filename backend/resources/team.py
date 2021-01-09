from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required , get_jwt_identity

from models.team import TeamModel 

class Team(Resource): 
    @jwt_required
    def get(self,_idTeam):
        team = TeamModel.find_by_id(_idTeam)
        if team: 
            if TeamModel.is_in_team(get_jwt_identity(),team['admin'],team['users']):
                team = TeamModel(team['_id'],team["name"],team["admin"],team["users"])
                return team.json(), 200
            else : 
                return {'message' : "No authorization"} , 401

        return {'message': 'Team not found'}, 400

class Teams(Resource): 
    @jwt_required
    def get(self):
        teams = TeamModel.find_all()
        if teams : 
            arrayTeam = []
            for team in teams:
                if TeamModel.is_in_team(get_jwt_identity(),team['admin'],team['users']):
                    newTeam = TeamModel(team['_id'],team["name"],team["admin"],team["users"])
                    arrayTeam.append(newTeam.json())
        
            return arrayTeam , 200

        return {'message' : 'Any team'} , 400

