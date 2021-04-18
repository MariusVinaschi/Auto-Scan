from pydantic import BaseModel
from typing import List, Optional


class input_responder(BaseModel): 
    scan_name : str
    list_target: List[str]
    interface : str
    our_ip : str


class result_responder(BaseModel):
    scan_name : str
    list_target : List[str]
    result : Optional[list] = []
    