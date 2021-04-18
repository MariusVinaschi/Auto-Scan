import subprocess
from pathlib import Path
import re 

class ntlmv2():
    def __init__(self, username, domain, full_hash, path_list_password):
        self.username = username
        self.domain = domain
        self.full_hash = full_hash
        self.path_list_password = path_list_password
        self.type_john_hash = 'netntlmv2'
        self.name_file = 'password_file.txt'
        
    def start_john_ntlmv2(self):

        if not self._isFile_exist(self.path_list_password):
            return {'Errors': 'No list of password'}

        result_crack_hash = self._crack_hash()

        ###### Error during the crack hash ##### 
        if 'Errors' in result_crack_hash.keys(): 
            if result_crack_hash['Errors'] == 'No password found':
                return {'domain': self.domain, 'username':self.username,'password':''}
            return result_crack_hash

    def _crack_hash(self):
        listJohn = ["john", "--format="+str(self.type_john_hash), "--wordlist="+str(self.path_list_password), str(self.name_file)]

        output = subprocess.run(listJohn,capture_output=True, text=True)
        
        if output.returncode != 0 :
            return {'Errors':'Error during the execution of John CrackHash'}
        
        if len(output.stdout.splitlines()) > 1:
            return {'Results': output.stdout.splitlines()[1]} 

        return {'Errors':'No password found'}

    # parse the output 
    def _parse_result_crack_hash(self, result_crack_hash): 
        regex_crack_hash = r'^([^\s]{1,}) *([^\s]{1,})$'
        if re.match(regex_crack_hash,result_crack_hash):
            return {'domain':self.domain,'username':self.username,'password':result_crack_hash.split()[0]}

        return {'Errors':'Error during the parsing of hash crack'}

    # if password have already crack 
    def _show_previous_hash_crack(self):
        listJohn = ["john", "--format="+str(self.type_john_hash), "--show", str(self.name_file)]
        
        output = subprocess.run(listJohn,capture_output=True, text=True)

        if output.returncode != 0 :
            return {'Errors':'Error during the execution of John show Hash'}
        return {'Results':output.stdout.splitlines()[0]}

    # parse the result 
    def _parse_result_previous_hash_crack(self,result_previous_hash_crack): 
        regex_previous_hash_crack = r'^.{0,}:(.{0,}):.{0,}:.{0,}:.{0,}:.{0,}$'

        if re.match(regex_previous_hash_crack,result_previous_hash_crack): 
            groups = re.match(regex_previous_hash_crack,result_previous_hash_crack).groups()
            return {'domain': self.domain ,'username':self.username ,'password':groups[0]}

        return {'Errors':'Error during the parsing of previous hash crack'}

    # Create file to stock password
    def _create_file(self):
        f = open(self.name_file,'w')
        f.write(str(self.full_hash))
        f.close()

    # check if file exist
    def _isFile_exist(self, pathFile):
        if Path(pathFile).is_file(): 
            return True 

        return False