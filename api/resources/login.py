from flask import request
from flask_restful import Resource 
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token , jwt_required , get_raw_jwt

from blacklist import BLACKLIST
from schema.login import LoginSchema
from models.user import UserModel

class Login(Resource): 
    def post(self):
        errors = LoginSchema().validate(request.get_json())

        if errors:
            return {'message' : errors} , 400

        user = UserModel.find_by_mail(request.get_json()['mail'])
        
        if not user: 
            return {'message' : 'User not found'},400
        
        if not safe_str_cmp(user['password'],request.get_json()['password']):
            return {'message':'Invalid Credentials'},401
            
        access_token = create_access_token(identity=str(user['_id']),fresh=True)
        return {   
            'access_token': access_token ,
            'name' : user['name'] ,
            'surname' : user["surname"] , 
            'mail' : user['mail'] , 
            'job' : user['job'] , 
            'ipMsfrpcd': user['server']['ip']
        },200

class Logout(Resource):
    @jwt_required 
    def post(self): 
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message':'Successfully logged out'} , 200 
