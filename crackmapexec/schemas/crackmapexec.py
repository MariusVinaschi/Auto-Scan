from marshmallow import Schema , fields , validate , validates, ValidationError

class cme_schema(Schema):
    scan_name  = fields.String(required=True, validate=[validate.Length(2,99)])
    list_target =   fields.List(fields.String(),required = True)
    domain = fields.String(required=True) 
    username = fields.String(required=True)
    password = fields.String(required=True)
