from flask import Flask, request

from schemas.crackmapexec import cme_schema
from models.custom_crackmapexec import CrackMapExec
app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        errors = cme_schema().validate(request.get_json())
        if errors:
            return {"message" : "Problem with Inputs" , "errors" : errors} , 400

        cme = request.get_json()

        new_cme_scan = CrackMapExec(cme['scan_name'], cme['list_target'], cme["username"], cme['password'], cme["domain"], 'smb')
        new_cme_scan.start_crackmapexec()
        result_crackmapexec = new_cme_scan.get_results()
        
        return {
            'scan_name':cme['scan_name'],
            'list_target': result_crackmapexec['list_target'],
            'computers' : result_crackmapexec['computers'],
            'users' : result_crackmapexec['users'],
            'groups': result_crackmapexec['groups'],
            'shares': result_crackmapexec['shares']
        },200
    else:
        return {'Message':'Docker cme is alive'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)