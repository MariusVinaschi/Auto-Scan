from typing import Optional
from fastapi import FastAPI
import logging
from impacket import version
from impacket.examples import logger


from app.depedency.GetADUsers import GetADUsers, create_args_getadusers
from app.depedency.GetUserSPNs import GetUserSPNs, create_args_getusersspns
from app.depedency.Samrdump import SAMRDump, create_args_samrdump
from app.depedency.Lookupsid import LSALookupSid, create_args_lookupsid

from app.schemas.impacket import input_impacket, input_impacket_only_dc, result_samrdump, result_getuserspns, result_lookupsid, result_getadusers

app = FastAPI()

@app.get('/',status_code=200)
def is_alive():
    return {'Message':'Docker impacket is alive'}

# Just need to launch on Domain Controller 
@app.post('/getadusers', response_model=result_getadusers, status_code=200)
def start_getadusers(options_impacket : input_impacket_only_dc):
    
    domain = options_impacket.domain
    if '.local' not in domain:
        domain += '.local'
   
    options = create_args_getadusers(options_impacket.domain_controler_ip, options_impacket.domain, options_impacket.username, options_impacket.password, True)
    # Init the example's logger theme
    logger.init(options.ts)

    if options.debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
        # Print the Library's installation path
        logging.debug(version.getInstallationPath())
    else:
        logging.getLogger().setLevel(logging.INFO)

    list_user = []

    try:
        executer = GetADUsers(options_impacket.username, options_impacket.password, domain, options)
        list_user = executer.run()
    except Exception as e:
        if logging.getLogger().level == logging.DEBUG:
            import traceback
            traceback.print_exc()
        print((str(e)))

    return { 
        'scan_name': options_impacket.scan_name,
        'domain_controler_ip': options_impacket.domain_controler_ip,
        'list_user': list_user
    }

@app.post('/getuserspns', response_model=result_getuserspns, status_code=200)
def start_getuserspns(options_impacket : input_impacket_only_dc):
    # Init the example's logger theme
    logger.init()

    domain = options_impacket.domain

    if '.local' not in domain:
        domain += '.local'

    targetDomain = domain

    options = create_args_getusersspns(options_impacket.domain_controler_ip, options_impacket.domain, options_impacket.username, options_impacket.password)

    if options.debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
        # Print the Library's installation path
        logging.debug(version.getInstallationPath())
    else:
        logging.getLogger().setLevel(logging.INFO)

    list_services = []

    try:
        executer = GetUserSPNs(options_impacket.username, options_impacket.password, domain, targetDomain, options)
        list_services = executer.run()
    except Exception as e:
        if logging.getLogger().level == logging.DEBUG:
            import traceback
            traceback.print_exc()
        logging.error(str(e))

    return {
        "scan_name" : options_impacket.scan_name,
        "domain_controler_ip" : options_impacket.domain_controler_ip,
        "list_services" : list_services
    }

@app.post('/samrdump', response_model=result_samrdump, status_code=200)
def start_samrdump(options_impacket : input_impacket):
    
    domain = options_impacket.domain
    port = "445"

    if '.local' not in domain:
        domain += '.local'

    options = create_args_samrdump(domain, options_impacket.username, options_impacket.password, options_impacket.domain_controler_ip, options_impacket.target_ip, port)

    # Init the example's logger theme
    logger.init(options.ts)

    if options.debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
        # Print the Library's installation path
        logging.debug(version.getInstallationPath())
    else:
        logging.getLogger().setLevel(logging.INFO)


    if options.target_ip is None:
        options.target_ip = options_impacket.domain_controler_ip

    list_user = []
    dumper = SAMRDump(options_impacket.username, options_impacket.password, domain, options.hashes, options.aesKey, options.k, options.dc_ip, int(options.port), options.csv)
    list_user = dumper.dump(options_impacket.domain_controler_ip, options.target_ip)
    
    return {
        'scan_name': options_impacket.scan_name,
        'target_ip' : options.target_ip,
        'list_user' : list_user
    }

@app.post('/lsalookupsid', response_model=result_lookupsid, status_code=200)
def start_lsalookupid(options_impacket : input_impacket):
    domain = options_impacket.domain

    if '.local' not in domain:
        domain += '.local'
        
    options = create_args_lookupsid(domain, options_impacket.username, options_impacket.password, options_impacket.domain_controler_ip, options_impacket.target_ip)
    # Init the example's logger theme
    logger.init(options.ts)

    if options.target_ip is None:
        options.target_ip = options_impacket.domain_controler_ip

    list_user = []

    lookup = LSALookupSid(options_impacket.username, options_impacket.password, domain, int(options.port), options.hashes, options.domain_sids, options.maxRid)
    try:
        list_user = lookup.dump(options_impacket.domain_controler_ip, options.target_ip)
    except:
        pass

    return {
        'scan_name' : options_impacket.scan_name,
        'target_ip' : options.target_ip,
        'list_user' : list_user
    }

