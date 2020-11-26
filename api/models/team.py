from bson.objectid import ObjectId
from bson import json_util 
import json

from .user import UserModel

class TeamModel():
    def __init__(self, _id, name, admin, users):
        self._id = _id
        self.name = name
        self.admin = admin
        self.users = users

    def json(self):
        return {
            "id" : str(self._id),
            "name" : self.name,
            "admin" : self.find_admin(),
            "users" : self.find_users()
        }

    def find_admin(self):
        admin = UserModel.find_by_id(json.loads(json_util.dumps(self.admin))["$oid"])
        if admin: 
            return UserModel(admin["name"],admin["surname"],admin["mail"],admin["job"],admin['server']['ip']).json()
        return {}
    
    def find_users(self):
        from app import mongo
        arrayUsers = []
        for user in self.users:
            userId = json.loads(json_util.dumps(user))
            arrayUsers.append(ObjectId(userId['$oid']))

        users = mongo.db.Users.find({ "_id": { "$in": arrayUsers } })
        
        arrayUsers = []
        for user in users:
            arrayUsers.append(UserModel(user["name"],user["surname"],user["mail"],user["job"],user['server']['ip']).json())
            
        return arrayUsers

    @classmethod
    def find_by_id(cls,_idTeam):
        from app import mongo 
        return mongo.db.Teams.find_one({'_id': ObjectId(_idTeam)})
    
    @classmethod 
    def find_all(cls): 
        from app import mongo
        return mongo.db.Teams.find()

    @classmethod 
    def is_in_team(cls,idUser, admin, users):
        arrayUsers = []
        for user in users:
            arrayUsers.append(str(user))
        
        arrayUsers.append(str(admin))

        if str(idUser) in arrayUsers: 
            return True
        
        return False