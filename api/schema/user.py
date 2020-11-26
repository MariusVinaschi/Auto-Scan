from marshmallow import Schema , fields , validate , validates, ValidationError
import re

class UserSchema(Schema):
    surname = fields.String(required=True, validate=[validate.Length(2,30), validate.Regexp(r"^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$")])
    name = fields.String(required = True, validate = [ validate.Length(2,30), validate.Regexp(r"^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$")])
    mail = fields.Email(required=True)
    job = fields.String(required=True, validate=validate.Length(2,60))
    ipmsfrpcd = fields.String(required=True,validate=validate.Length(7,20))
    passwordmsfrpcd = fields.String(required=True,validate=validate.Length(4,20))

