export interface teamApiInterface {
    id: string,
    name : string, 
    admin : userApiInterface,
    users : userApiInterface[],
}

export interface userApiInterface { 
    surname: string ,
    name : string, 
    mail : string, 
    job : string, 
    ipMsfrpcd : string 
}

export interface NmapInterface {
    "port":string, 
    "service":string
}

export interface ModuleInterface {
    'name':string ,
    'results': string[]
}

export interface MetasploitInterface{ 
    "port": string,
    "modules": ModuleInterface[]
}

export interface ScansApiInterface {
    "id": string,
    "name": string,
    "ip": string,
    "user": {
        "surname": string,
        "name": string
    },
    "team": {
        "name": string 
    },
    "date": string,
    "nmap": NmapInterface[]
}

export interface ScanApiInterface {
    "id": string,
    "name": string,
    "ip": string,
    "user": userApiInterface,
    "team": teamApiInterface,
    "date": string, 
    "nmap": NmapInterface[]
    "metasploit": MetasploitInterface[]
}