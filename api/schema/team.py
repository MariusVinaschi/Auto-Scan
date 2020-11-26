from marshmallow import Schema , fields , validate , validates, ValidationError
import re

class TeamSchema(Schema):
    name : fields.String(required = True, validate = [ validate.Length(2,20), validate.Regexp(r"^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$")])