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
    port : string, 
    service:string
}

export interface ModuleInterface {
    name: string ,
    results: string[]
}

export interface MetasploitInterface{ 
    port: string,
    modules: ModuleInterface[]
}

// ---------------- METASPLOIT Scan ------------------ // 

export interface ScansApiInterface {
    id: string,
    name: string,
    ip: string,
    user: {
        surname: string,
        name: string
    },
    team: {
        name: string 
    },
    date: string,
    nmap: NmapInterface[]
}

export interface ScanApiInterface {
    id: string,
    name: string,
    ip: string,
    user: userApiInterface,
    team: teamApiInterface,
    date: string, 
    nmap: NmapInterface[]
    metasploit: MetasploitInterface[]
}

// ----------- ACTIVE DIRECTORY -------------- // 
export interface ScanAdApiInterface { 
    id : string,
    name:string,
    list_target :string[],
    user:userApiInterface,
    team:teamApiInterface,
    date:string,
    hosts:any[],
    domain:any,
    credentials:CredentialsInterface[],
}

export interface ScansAdApiInterface {
    id:string,
    name:string,
    list_target :string[],
    user: {
        surname: string,
        name: string
    },
    team: {
        name: string 
    },
    date: string,
    domain:DomainInterface,
}

// --------------- Domain -------------------- // 

export interface DomainInterface {
    name : string,
    domain_controler_ip : string,
    domain_controler_name : string,
    users : UsersDomainInterface[],
    groups : GroupsDomainInterface[],
    services : ServicesDomainInterface[]
}

export interface UsersDomainInterface {
    username : string,
    password : string,
    mail : string,
    password_last_set : string,
    last_logon : string
}

export interface GroupsDomainInterface {
    name: string 
}

export interface ServicesDomainInterface {
    service_principal_name : string, 
    name : string,
    member_of : string,
    password_last_set : string,
    last_logon : string,
    delegation : string,
}

// ---------- Credentials ------------ // 

export interface CredentialsInterface{
    ip:string,
    domain:string,
    username:string,
    password:string,
}

// ---------- Hosts ------------------- // 

export interface HostsInterface {
    IP : string,
    name : string,
    Ports : PortsInterface[], 
    users: UsersHostsInterface[],
    shares : SharesHostsInterface[]
    domain_controller? :string
}

export interface PortsInterface {
    portid : string,
    service : string,
    product? : string,
    extrainfo? : string
}

export interface UsersHostsInterface {
    username : string,
    uid : string,
    fullname : string,
    primary_group_id : string,
    bad_password_count : string,
    logon_count : string,
    password_last_set : string,
    is_expire : string,
    is_disable : string,
    comment : string
}

export interface SharesHostsInterface {
    share : string,
    privs : string,
    comment : string
}