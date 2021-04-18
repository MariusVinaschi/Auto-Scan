import logging
import os
from pprint import pformat
from socket import timeout  
import sqlite3
import shutil
import configparser
from argparse import Namespace
from gevent.pool import Pool # Threading

from models.CrackMapExec.cme.logger import setup_logger, setup_debug_logger, CMEAdapter
from models.CrackMapExec.cme.loaders.protocol_loader import protocol_loader
from models.CrackMapExec.cme.first_run import first_run_setup
from models.CrackMapExec.cme.helpers.misc import identify_target_file
from models.CrackMapExec.cme.parsers.ip import parse_targets
from models.CrackMapExec.cme.parsers.nmap import parse_nmap_xml
from models.CrackMapExec.cme.parsers.nessus import parse_nessus_file
import models.CrackMapExec.cme.helpers.powershell as powershell
from models.CrackMapExec.cme.protocols.smb.database import database

CME_PATH = os.path.expanduser('~/.cme')
WS_PATH = os.path.join(CME_PATH, 'workspaces')
CONFIG_PATH = os.path.join(CME_PATH, 'cme.conf')

class CrackMapExec: 
    def __init__(self, scan_name, list_target, username, password, domain , protocol):
        self.scan_name = scan_name
        self.list_target = list_target
        self.username = username
        self.password = password 
        self.domain = domain 
        self.protocol = protocol

    def start_crackmapexec(self):
        # Init for CME 
        # First run create file and verify config 
        # Logger to have history of command
        setup_logger()
        logger = CMEAdapter()
        first_run_setup(logger)

        # Create the workspace where .db will be stock
        self.create_workspace(logger)
        self.modify_conf_file_cme()

        args = self.create_args()
  
        # read the config file 
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        targets = []

        # define the workspace
        current_workspace = config.get('CME', 'workspace')

        if args.verbose:
            setup_debug_logger()

        logging.debug('Passed args:\n'+ pformat(vars(args)))

        self.check_attr(args,targets)

        p_loader = protocol_loader()

        # give the path of smb.py and smb_db.py
        protocol_path = p_loader.get_protocols()[args.protocol]['path']
        protocol_db_path = p_loader.get_protocols()[args.protocol]['dbpath']
        protocol_db_object = getattr(p_loader.load_protocol(protocol_db_path), 'database')
        p_loader_test = p_loader.load_protocol(protocol_path)
        protocol_object = getattr(p_loader_test,str(args.protocol))
        
        # DB Connection
        db_path = os.path.join(WS_PATH,str(current_workspace),str(args.protocol)+'.db')
        db_connection = sqlite3.connect(db_path, check_same_thread=False)
        db_connection.text_factory = str
        db_connection.isolation_level = None
        db = protocol_db_object(db_connection)

        # Give args to protocol_object
        setattr(protocol_object,'config',config)

        pool = Pool(args.threads)
        jobs = []

        for target in targets:
            jobs.append(pool.spawn(protocol_object,args,db,str(target)))

        for job in jobs:
            job.join(timeout=args.timeout)

    def modify_conf_file_cme(self): 
        # Check if file Exist 
        if os.path.exists(CONFIG_PATH): 
            # Read file 
            parser = configparser.ConfigParser()
            parser.read(CONFIG_PATH)
            
            # Write Config File 
            if 'CME' in parser.sections():
                if 'workspace' in parser['CME']:
                    parser.set('CME','workspace',str(self.scan_name))

                    with open(CONFIG_PATH, 'w') as configfile:
                        parser.write(configfile)

    def create_workspace(self,logger):
        # If Exist remove Folder
        if os.path.exists(os.path.join(WS_PATH,str(self.scan_name))):
            shutil.rmtree(os.path.join(WS_PATH,str(self.scan_name)))
        
        # Create Folder  
        os.mkdir(os.path.join(WS_PATH,str(self.scan_name)))

        # Load Protocol and create .db file for all protocol
        p_loader = protocol_loader()
        protocols = p_loader.get_protocols()
        for protocol in protocols.keys():
            try:
                protocol_object = p_loader.load_protocol(protocols[protocol]['dbpath'])
            except KeyError:
                continue

            proto_db_path = os.path.join(WS_PATH, str(self.scan_name), protocol + '.db')

            if not os.path.exists(proto_db_path):
                logger.info('Initializing {} protocol database'.format(protocol.upper()))
                conn = sqlite3.connect(proto_db_path)
                c = conn.cursor()

                # try to prevent some of the weird sqlite I/O errors
                c.execute('PRAGMA journal_mode = OFF')
                c.execute('PRAGMA foreign_keys = 1')

                getattr(protocol_object, 'database').db_schema(c)

                # commit the changes and close everything off
                conn.commit()
                conn.close()

    def create_args(self):
        username = self.change_to_list(self.username)
        password = self.change_to_list(self.password)
        list_target = self.change_to_list(self.list_target)
        
        args = Namespace(
            aesKey=None, 
            clear_obfscripts=False, 
            content=False, 
            continue_on_success=False, 
            cred_id=[], 
            darrell=False, 
            depth=None, 
            disks=False, 
            exclude_dirs='', 
            exec_method=None, 
            execute=None, 
            fail_limit=None, 
            force_ps32=False, 
            gen_relay_list=None, 
            get_file=None, 
            gfail_limit=None, 
            groups='', 
            hash=[], 
            jitter=None, 
            kdcHost=None, 
            kerberos=False, 
            list_modules=False, 
            local_auth=False, 
            local_groups=None, 
            loggedon_users=False, 
            lsa=False, 
            module=None,
            module_options=[], 
            no_bruteforce=False, 
            no_output=False, 
            ntds=None, 
            obfs=False, 
            only_files=False, 
            pattern=None, 
            port=445,
            ps_execute=None, 
            put_file=None, 
            regex=None, 
            rid_brute=None, 
            sam=False, 
            server='https', 
            server_host='0.0.0.0', 
            server_port=None, 
            share='C$', 
            show_module_options=False, 
            spider=None, 
            spider_folder='.', 
            threads=100, 
            timeout=30, 
            ufail_limit=None, 
            users='', 
            verbose=False, 
            wmi=None, 
            wmi_namespace='root\\cimv2',
            protocol=str(self.protocol), # After this line Important options
            smb_server_port=445, 
            domain=str(self.domain), 
            username=username, 
            password=password,
            target=list_target, 
            shares=False, # Search Shares 
            sessions=False, # Search Sessions
            pass_pol=False
        )

        return args  

    def change_to_list(self, param):
        new_list = []
        
        if isinstance(param,str):
            new_list.append(param)
            return new_list
        
        new_list = param

        return new_list

    def check_attr(self,args,targets):
        if hasattr(args, 'username') and args.username:
            for user in args.username:
                if os.path.exists(user):
                    args.username.remove(user)
                    args.username.append(open(user, 'r'))

        if hasattr(args, 'password') and args.password:
            for passw in args.password:
                if os.path.exists(passw):
                    args.password.remove(passw)
                    args.password.append(open(passw, 'r'))

        elif hasattr(args, 'hash') and args.hash:
            for ntlm_hash in args.hash:
                if os.path.exists(ntlm_hash):
                    args.hash.remove(ntlm_hash)
                    args.hash.append(open(ntlm_hash, 'r'))

        if hasattr(args, 'target') and args.target:
            for target in args.target:
                if os.path.exists(target):
                    target_file_type = identify_target_file(target)
                    if target_file_type == 'nmap':
                        targets.extend(parse_nmap_xml(target, args.protocol))
                    elif target_file_type == 'nessus':
                        targets.extend(parse_nessus_file(target, args.protocol))
                    else:
                        with open(target, 'r') as target_file:
                            for target_entry in target_file:
                                targets.extend(parse_targets(target_entry.strip()))
                else:
                    targets.extend(parse_targets(target))

    def get_results(self):
        # Connection to the database
        db_path = os.path.join(WS_PATH,str(self.scan_name),str(self.protocol)+'.db')
        conn = sqlite3.connect(db_path , check_same_thread=False )
        conn.text_factory = str
        conn.isolation_level = None

        result_dict = {
            'scan_name': self.scan_name,
            'list_target' : self.list_target,
            'computers' : [],
            'users' : [],
            'groups' : [],
            'shares' : []
        }

        db_smb = database(conn)
        users = db_smb.get_users()
        result_dict['users'] = self.parse_users(users)
        
        groups = db_smb.get_groups()
        result_dict['groups'] = self.parse_groups(groups)

        computers = db_smb.get_computers()
        result_dict['computers'] = self.parse_computers(computers)
        
        return result_dict

    def parse_users(self,users):
        list_users = []

        for user in users: 
            dict_user = {
                'domain' : user[1],
                'username' : user[2],
                'password' : user[3]
            }
            list_users.append(dict_user)

        return list_users

    def parse_computers(self,computers):
        list_computer = []
        for computer in computers:
            dict_computer = {
                'ip':computer[1],
                'hostname':computer[2],
                'domain':computer[3],
                'os':computer[4],
                'dc' : computer[5]
            }
            list_computer.append(dict_computer)            
        return list_computer

    def parse_groups(self,groups):
        list_groups = []
        for group in groups:
            dict_group = {
                'domain':group[1],
                'name': group[2]
            }
            list_groups.append(dict_group)

        return list_groups

    def parse_shares(self,shares):
        print('Parse shares')