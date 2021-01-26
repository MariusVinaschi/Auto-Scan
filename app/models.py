from pydantic import BaseModel
from typing import List

class exempleModel(BaseModel):
    id : int 

class returnModel(BaseModel): 
    text : str 