from flask_restful import Resource
from flask import request 
from flask_jwt_extended import jwt_required , get_jwt_identity

from schema.user import UserSchema
from models.user import UserModel

class User(Resource): 
    @jwt_required
    def get(self): 
        user = UserModel.find_by_id(get_jwt_identity())
        if user:
            user = UserModel(user["surname"],user["name"],user["mail"],user["job"],user['server']['ip'])
            return user.json() , 200

        return {'message': 'User not found'}, 400

    
    @jwt_required
    def post(self): 
        errors = UserSchema().validate(request.get_json())

        if errors : 
            return {"message" : errors} , 400
        
        user = UserModel(
            request.get_json()["surname"],
            request.get_json()["name"],
            request.get_json()["mail"],
            request.get_json()["job"],
            request.get_json()['ipmsfrpcd'],
            request.get_json()['passwordmsfrpcd']
        )
        try : 
            user.modifyUser(get_jwt_identity())
        except:
            return {"message": "An error occurred modifying the user."}, 500

        return user.json() , 201

        