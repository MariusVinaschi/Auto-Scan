import subprocess
from pathlib import Path
import re 

class John():
    def __init__(self, username, hash_password, path_list_password, type_john_hash):
        self.username = username
        self.hash_password = hash_password
        self.path_list_password = path_list_password
        self.type_john_hash = type_john_hash
        self.name_file = 'password_file.txt'

    def main(self):
        self._create_file()
        
        if not self._isFile_exist(self.path_list_password):
            return {'Errors': 'No list of password'}

        result_crack_hash = self._crack_hash()

        ###### Error during the crack hash ##### 
        if 'Errors' in result_crack_hash.keys(): 
            if result_crack_hash['Errors'] == 'No password found':
                return {'username':self.username,'password':''}
            return result_crack_hash

        ###### Need to use the option --show ###### 
        if result_crack_hash['Results'] == "No password hashes left to crack (see FAQ)":
            result_previous_hash_crack = self._show_previous_hash_crack()
            
            if 'Errors' in result_previous_hash_crack.keys():
                return result_previous_hash_crack

            return self._parse_result_previous_hash_crack(result_previous_hash_crack['Results'])
    
        ###### Parse the crack hash ######
        return self._parse_result_crack_hash(result_crack_hash['Results'])

    # crack the hash 
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
            return {'username':self.username,'password':result_crack_hash.split()[0]}

        return {'Errors':'Error during the parsing of hash crack'}
        
    # if password have already crack 
    def _show_previous_hash_crack(self):
        listJohn = ["john", "--format="+str(self.type_john_hash), "--show", str(self.name_file)]
        
        output = subprocess.run(listJohn,capture_output=True, text=True)

        if output.returncode != 0 :
            return {'Errors':'Error during the execution of John show Hash'}
        print(output.stdout)
        return {'Results':output.stdout.splitlines()[0]}

    # parse the result 
    def _parse_result_previous_hash_crack(self,result_previous_hash_crack): 
        regex_previous_hash_crack = r'^(.{0,}):(.{0,})$'

        if re.match(regex_previous_hash_crack,result_previous_hash_crack): 
            groups = re.match(regex_previous_hash_crack,result_previous_hash_crack).groups()
            print(groups)
            return {'username': groups[0],'password':groups[1]}

        return {'Errors':'Error during the parsing of previous hash crack'}

    # Create file to stock password
    def _create_file(self):
        f = open(self.name_file,'w')
        f.write(self.username+':'+self.hash_password)
        f.close()

    # check if file exist
    def _isFile_exist(self, pathFile):
        if Path(pathFile).is_file(): 
            return True 

        return False