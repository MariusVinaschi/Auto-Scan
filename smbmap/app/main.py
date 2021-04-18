from typing import Optional
from fastapi import FastAPI

from app.schemas.smbmap import scan_smbmap_schema, result_smbmap_schema
from app.depedency.custom_smbmap import custom_SMBMAP

app = FastAPI()

@app.get('/',status_code=200)
def is_alive():
    return {'Message':'Docker smbmap is alive'}

@app.post('/',response_model=result_smbmap_schema, status_code=200)
async def start_smbmap(scan_smbmap : scan_smbmap_schema):

    hosts = []

    smbmap = custom_SMBMAP(scan_smbmap.scan_name, scan_smbmap.list_target, scan_smbmap.domain, scan_smbmap.username, scan_smbmap.password)
    
    # Create the file targets.txt
    smbmap.create_target_file()

    # Create the object for args
    object_hostfiles = open(smbmap.name_targets_file, "r", encoding="utf-8")
    
    # Without Option to get all the shares
    option_dir_list = None
    output_file = 'output_without_option.csv'
    
    args = smbmap.create_args(object_hostfiles,option_dir_list,output_file)
    
    # Start smbmap 
    smbmap.launch_smbmap(args)
    # parse the output
    hosts = smbmap.parse_output_file(output_file)
    # remove file 
    smbmap.remove_file(output_file)

    return { 
        'scan_name':scan_smbmap.scan_name,
        'list_target': scan_smbmap.list_target,
        'hosts':hosts
    }