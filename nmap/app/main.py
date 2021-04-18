from fastapi import FastAPI, Depends

from app.schemas.scan import Scan_schema, Nmap_schema
from app.depedency.portscan import PortScan

app = FastAPI()

@app.get('/',status_code=200)
def is_alive():
    return {'Message':'Docker nmap is alive'}


@app.post('/',response_model=Nmap_schema,status_code=200)
def start_nmmap(scan : Scan_schema):
    new_scan = PortScan(scan.scan_name)
    scan_result = new_scan.startNmap(scan.list_target)
    
    if scan_result != False: 
        return {
            'result': True,
            'scan_name': scan.scan_name,
            'hosts': scan_result['hosts']
        }

    return {
        'result': False,
        'scan_name': scan.scan_name,
    }
