from pydantic import BaseModel
from typing import List, Optional

class scan_smbmap_schema(BaseModel):
    scan_name: str 
    list_target : List[str]
    domain : str
    username : str
    password : str

class result_smbmap_schema(BaseModel):
    scan_name : str
    list_target : List[str]
    hosts : Optional[List[dict]] = []
