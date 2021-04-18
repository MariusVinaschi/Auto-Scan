from pydantic import BaseModel
from typing import List, Optional

class input_john(BaseModel):
    username : str
    hash : str
    type_john_hash :str

class input_ntlmv2(BaseModel):
    username : str
    domain:str
    hash : str

class result_john(BaseModel):
    username : str
    password : str
