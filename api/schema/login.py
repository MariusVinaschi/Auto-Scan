from marshmallow import Schema , fields , validate , validates, ValidationError
import re

class LoginSchema(Schema):
    mail = fields.Email(required=True)
    password = fields.String(required=True , validate=validate.Length(5,30))


