from pydantic import BaseModel
from typing import List, Optional

class Scan_schema(BaseModel):
    scan_name: str
    list_target: List[str] = []

class Nmap_schema(BaseModel): 
    result:bool
    scan_name : str
    hosts : Optional[List[dict]] = []
