import os 

from flask import Flask , jsonify
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

from resources.login import Login , Logout
from resources.scan import Scan , Scans , NewScan
from resources.team import Team , Teams
from resources.user import User 
from resources.server import Server 
from blacklist import BLACKLIST 

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']
mongo = PyMongo(app)
api = Api(app)

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

##### Login ######
api.add_resource(Login,'/login')

##### Scan ######
api.add_resource(NewScan,'/newScan')
api.add_resource(Scan,'/scan/<string:_idScan>')
api.add_resource(Scans,'/scans')

##### Team ######
api.add_resource(Team,'/team/<string:_idTeam>')
api.add_resource(Teams,'/teams')

##### Users #####
api.add_resource(User,'/user')

##### Server #####
api.add_resource(Server,'/server')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
    
