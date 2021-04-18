from pydantic import BaseModel
from typing import List, Optional

class input_impacket(BaseModel):
    scan_name : str
    domain : str
    domain_controler_ip : str
    username : str
    password : str
    target_ip : Optional[str]

class input_impacket_only_dc(BaseModel):
    scan_name : str
    domain : str
    domain_controler_ip : str
    username : str
    password : str

class result_lookupsid(BaseModel):
    scan_name : str
    target_ip : str
    list_user : Optional[List] = []

class result_getuserspns(BaseModel):
    scan_name : str
    domain_controler_ip : str
    list_services : Optional[List] = []

class result_samrdump(BaseModel):
    scan_name : str
    target_ip : str
    list_user : Optional[List] = []

class result_getadusers(BaseModel):
    scan_name : str
    domain_controler_ip : str
    list_user : Optional[List] = []