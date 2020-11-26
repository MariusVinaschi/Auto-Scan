from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required , get_jwt_identity

from models.user import UserModel
from models.server import ServerModel

class Server(Resource): 
    @jwt_required
    def get(self): 
        user = UserModel.find_by_id(get_jwt_identity())
        if user:
            server = ServerModel(user['server']['ip'],user['server']['password'])
            if server.check_Connect(server.Connect()):
                return {"Message" : "Connect to the MSFRPCD server"} , 201 
            else: 
                return {"Message": "Unable to connect to the MSFRPCD server"},404
        else:
            return {"Message" : "User not found"} , 404


    # Test connection to server MSFRPCD