import {createContext} from 'react'

export interface UserInterface  {
    'access_token' : string, 
    'surname' : string, 
    'name' : string,
    'mail' : string, 
    'job' : string, 
    'ipMsfrpcd' : string 
}

interface context {
    User: UserInterface | null ;
    setUser: React.Dispatch<React.SetStateAction<UserInterface>>;
}


    
export const UserContext = createContext<any>(null)
