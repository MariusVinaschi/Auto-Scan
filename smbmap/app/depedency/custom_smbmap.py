#!/usr/bin/env python3
from argparse import Namespace
import socket
from multiprocessing import Pool
import sys
import os
import csv

from app.depedency.smbmap.smbmap import SMBMap, Loader, find_open_ports, login

class custom_SMBMAP:
    def __init__(self, scan_name, targets, domain,username, password):
        self.scan_name = scan_name
        self.targets = targets
        self.domain = domain
        self.username = username
        self.password = password
        self.name_targets_file = 'targets.txt'

    def launch_smbmap(self, args):
        hosts = []

        mysmb = SMBMap()
        mysmb.loader = Loader()
        mysmb.loading = True
        mysmb.loader.start()

        lsshare = False
        lspath = False

        if args.csv:
            mysmb.csv = args.csv
            mysmb.outfile = open(args.csv, 'w')
            if args.recursive_dir_list != None or args.dir_list != None:
                csv_fields = ['Host', 'Share', 'Privs', 'isDir', 'Path', 'fileSize', 'Date']
            else:
                csv_fields = ['Host', 'Share', 'Privs', 'Comment']
            mysmb.writer = csv.DictWriter(mysmb.outfile, csv_fields)
            mysmb.writer.writeheader()

        if args.verbose == False:
                mysmb.verbose = False
        else:
            VERBOSE = True

        if args.recursive_dir_list != None:
            mysmb.recursive = True
            mysmb.list_files = True
            try:
                lspath = args.recursive_dir_list.replace('/','\\').split('\\')
                lsshare = lspath[0]
                lspath = '\\'.join(lspath[1:])
            except:
                pass

        elif args.dir_list != None:
            mysmb.list_files = True
            try:
                lspath = args.dir_list.replace('/','\\').split('\\')
                lsshare = lspath[0]
                lspath = '\\'.join(lspath[1:])
            except:
                pass

        socket.setdefaulttimeout(3)

        if args.hostfile:
            porty_time = Pool(40)
            args.hostfile = porty_time.map(find_open_ports, args.hostfile)

        lmhash, nthash = ('', '')

        if args.hostfile:
            for ip in args.hostfile:
                if ip:
                    try:
                        hosts.append({ 'ip' : ip.strip(), 'name' : socket.getnameinfo((ip.strip(), args.port),0)[0] , 'port' : args.port, 'user' : args.user, 'passwd' : args.passwd, 'domain' : args.domain, 'lmhash' : lmhash, 'nthash' : nthash })
                    except:
                        hosts.append({ 'ip' : ip.strip(), 'name' : 'unknown', 'port' : 445, 'user' : args.user, 'passwd' : args.passwd, 'domain' : args.domain, 'lmhash' : lmhash, 'nthash' : nthash })
                        continue
        elif args.host and args.host.find('/') == -1:
            if find_open_ports(args.host.strip()):
                try:
                    hosts.append({ 'ip' : args.host.strip(), 'name' : socket.getnameinfo((args.host.strip(), args.port),0)[0], 'port' : args.port, 'user' : args.user, 'passwd' : args.passwd, 'domain' : args.domain, 'lmhash' : lmhash, 'nthash' : nthash})
                except:
                    hosts.append({ 'ip' : args.host.strip(), 'name' : 'unknown', 'port' : args.port, 'user' : args.user, 'passwd' : args.passwd, 'domain' : args.domain, 'lmhash' : lmhash, 'nthash' : nthash })

        connections = []
        login_worker = Pool(40)
        connections = login_worker.map(login, hosts)
        mysmb.hosts = { value['ip']:value for value in hosts }
        mysmb.smbconn = { conn.getRemoteHost():conn for conn in connections if conn is not False}
        counter = 0

        if mysmb.loading:
            mysmb.kill_loader()

        for host in list(mysmb.smbconn.keys()):
            is_admin = False
            try:
                if len(mysmb.smbconn[host].listPath('ADMIN$', mysmb.pathify('/'))) > 0:
                    is_admin = True
            except:
                pass
                

            mysmb.loader = Loader()
            mysmb.loading = True
            mysmb.loader.start()

            try:
                tmp = mysmb.get_shares(host)
                if not args.admin and tmp is not None:
                    mysmb.output_shares(host, lsshare, lspath, args.write_check, args.depth)

                if mysmb.loading:
                    mysmb.kill_loader()
                mysmb.loader = None
                try:
                    mysmb.logout(host)
                except:
                    pass

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('[!] Error: ', (exc_type, fname, exc_tb.tb_lineno))
                sys.stdout.flush()

        if args.grepable or args.csv:
            mysmb.outfile.close()
    # Create the args to pass to smbmap 
    def create_args(self, object_hostfile,option_dir_list,output_file):
        args = Namespace(
            admin=False,
            command=None,
            delFile=None,
            depth=5,
            dir_only=False,
            dlPath=None,
            exclude=None,
            file_content_search=None,
            grepable=False,
            host=None,
            list_drives=False,
            mode='wmi',
            pattern=None,
            port=445,
            prompt=False,
            recursive_dir_list=None,
            search_path='C:\\Users',
            search_timeout='300',
            share='C$',
            skip=False,
            upload=None,
            verbose=True,
            version=False,
            write_check=True,
            nobanner=True,
            nocolor=True,
            noupdate=False,
            hostfile=object_hostfile, # Need <_io.TextIOWrapper name='target.txt' mode='r' encoding='UTF-8'>,
            domain=str(self.domain), # Name of the domain
            user=str(self.username), # Username
            passwd=str(self.password), # Password
            csv=str(output_file), # Name of the csv file
            dir_list=option_dir_list  # to use the -r options
        )
        return args

    def create_target_file(self):
        text = ''

        if isinstance(self.targets,list):
            for target in self.targets:
                text += str(target)+'\n'

        if isinstance(self.targets,str):
            text = self.targets

        f = open(self.name_targets_file,'w')
        f.write(text)
        f.close()

    def parse_output_file(self, output_file):
        hosts = []
        # Check if the file exist 
        if os.path.isfile(output_file):
            # open the file 
            with open(output_file) as csv_file:
                csv_reader = csv.reader(csv_file,delimiter=',')
                # Loop on the lines of the file 
                for count,row in enumerate(csv_reader):
                    # Don't take the first one 
                    if count != 0:
                        # Check if host already is in the dict_result 
                        index = next((index for (index,dict_host) in enumerate(hosts) if dict_host["host"] == row[0]), None)
                        # Add to the dict
                        if index != None:
                            dict_share = { 'share':row[1],'privs':row[2],'comment': row[3]}
                            hosts[index]['shares'].append(dict_share)
                        else :
                            hosts.append({'host': str(row[0]),'shares':[{'share':row[1],'privs':row[2],'comment': row[3]}]})

        return hosts                      

    def remove_file(self, output_file):
        if os.path.isfile(output_file):
            os.remove(output_file)
        
        if os.path.isfile(self.name_targets_file):
            os.remove(self.name_targets_file)


    ##### Add this lines to collect all children folder #####

    # With the option -r list contents of directory, default is to list root of all shares
    # option_dir_list = ''
    # output_file = 'output_with_r_option.csv'
    # args = self.create_args(object_hostfiles,option_dir_list,output_file)
    # self.launch_smbmap(args)