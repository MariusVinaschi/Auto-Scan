from typing import Optional
from fastapi import FastAPI

try : 
    from app.schemas.responder import input_responder, result_responder
    from app.depedency.curstom_responder import Responder
except :
    from schemas.responder import input_responder, result_responder
    from depedency.curstom_responder import Responder

app = FastAPI()

@app.get('/',status_code=200)
def is_alive():
    return {'Message':'Docker responder is alive'}

@app.post('/',response_model=result_responder,status_code=200)
def launch_responder(options : input_responder):
    
    if options.our_ip == '':
        our_ip = None
    else : 
        our_ip = options.our_ip

    new_responder = Responder(options.scan_name, options.list_target, options.interface, our_ip)
    new_responder.make_settings()
    new_responder.init_database()
    new_responder.init_threading()
    list_result = new_responder.start_responder()

    return {
        "scan_name": options.scan_name,
        "list_target": options.list_target,
        "result": list_result
    }