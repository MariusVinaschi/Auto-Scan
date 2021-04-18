from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class ScanADSchema(Schema):
    scan_name = fields.String(required=True, validate = [ validate.Length(2,30), validate.Regexp(r"^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$")])
    list_target = fields.List(fields.String,required=True)
    team = fields.String(required=True, validate=[validate.Length(24),validate.Regexp(r'[a-z0-9]{24}$')])
