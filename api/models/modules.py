class ModulesModel():
    def __init__(self, name):
        self.name = name

    @classmethod
    def find_modules_name(cls, name):
        from app import mongo 
        return mongo.db.Modules.find_one({'name': name})