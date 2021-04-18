from typing import Optional
from fastapi import FastAPI

# from app.depedency.john import John
# from app.schemas.john import input_john, result_john

from app.depedency.ntlmv2 import ntlmv2
from app.schemas.john import input_john, result_john, input_ntlmv2

app = FastAPI()

@app.get('/')
def is_alive():
    return {'Message':'Docker John is alive'}

@app.post('/ntlmv2', status_code=200)
def start_john_ntlmv2(input_ntlmv2 : input_ntlmv2):

    # dict_password = '/app/depedency/passwordList.txt'

    dict_password = '/app/depedency/passwordList.txt'

    new_john = ntlmv2(input_ntlmv2.username, input_ntlmv2.domain, input_ntlmv2.hash ,dict_password)

    new_john._create_file()
        
    if not new_john._isFile_exist(new_john.path_list_password):
        return {'Errors': 'No list of password'}

    result_crack_hash = new_john._crack_hash()

    ###### Error during the crack hash ##### 
    if 'Errors' in result_crack_hash.keys(): 
        if result_crack_hash['Errors'] == 'No password found':
            return {'domain': new_john.domain, 'username':new_john.username,'password':''}
        return result_crack_hash

    ###### Need to use the option --show ###### 
    if result_crack_hash['Results'] == "No password hashes left to crack (see FAQ)":
        result_previous_hash_crack = new_john._show_previous_hash_crack()
        
        if 'Errors' in result_previous_hash_crack.keys():
            return result_previous_hash_crack

        return new_john._parse_result_previous_hash_crack(result_previous_hash_crack['Results'])

    ###### Parse the crack hash ######
    return new_john._parse_result_crack_hash(result_crack_hash['Results'])
