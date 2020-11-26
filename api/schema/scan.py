from marshmallow import Schema , fields , validate , validates, ValidationError
import re

class ScanSchema(Schema):
    name = fields.String(required = True, validate = [ validate.Length(2,30), validate.Regexp(r"^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$")])
    ip = fields.String(required= True , validate = [validate.Length(7,15), validate.Regexp(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")])
    team = fields.String(required = True, validate = [validate.Length(24) , validate.Regexp(r"^[a-z0-9]{24}$")]) 


