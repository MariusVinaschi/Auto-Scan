from bson.objectid import ObjectId

class UserModel():
    def __init__(self, surname, name, mail, job, ipMsfrpcd, passwordmsfrpcd = ""):
        self.surname = surname
        self.name = name
        self.mail = mail
        self.job = job 
        self.ipMsfrpcd = ipMsfrpcd
        self.passwordmsfrpcd = passwordmsfrpcd

    def json(self):
        return {
            "surname" : self.surname,
            "name" : self.name,
            "mail": self.mail,
            "job": self.job,
            "ipMsfrpcd": self.ipMsfrpcd,
        }
    
    @classmethod
    def find_by_id(cls,_idUser):
        from app import mongo 
        return mongo.db.Users.find_one({'_id': ObjectId(_idUser)})

    @classmethod 
    def find_by_mail(cls,mail):
        from app import mongo
        return mongo.db.Users.find_one({'mail':mail})

    def modifyUser(self,_idUser):
        from app import mongo
        mongo.db.Users.update_one({'_id': ObjectId(_idUser)},{
            "$set": {
                "surname" : self.surname,
                "name":self.name,
                "mail": self.mail,
                "job": self.job,
                "server":{
                    "ip": self.ipMsfrpcd,
                    "password": self.passwordmsfrpcd
                }
            }
        })
