import React , {useEffect , useContext, useState} from 'react'; 
import axios from 'axios';
import {match} from 'react-router-dom';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Grid , Typography} from '@material-ui/core';

import {UserContext} from '../Context/UserContext';
import TemplatePage from './TemplatePage';
import {ScanApiInterface , userApiInterface , teamApiInterface} from '../Interface/ApiInterface';
import BoxContainer from '../Component/BoxContainer';
import BasicInformation from '../Component/Scan/BasicInformation';
import NmapResult from '../Component/Scan/NmapResult';
import MetasploitResult from '../Component/Scan/MetasploitResult';

interface ParametersInterface{
    id : string, 
}

interface ScanProps {
    match?:match<ParametersInterface>
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        containerTitle : {
            marginTop : theme.spacing(1),
            marginBottom : theme.spacing(1), 
        },
        title : {
            margin: theme.spacing(2),
            paddingBottom : theme.spacing(2),
            paddingTop:theme.spacing(1),
            textAlign:'center',
            borderBottom: '1px solid white'
        },
        container : {
            minWidth:'100%'
        }, 
        portTitle : {
            textDecoration: 'underline'
        }

    })
);



const Scan = (props : ScanProps) => {
    const {User} = useContext(UserContext)    
    const [Scan, setScan] = useState<ScanApiInterface>(initialValuesScan)
    const classes = useStyles();

    useEffect(() => {
        var scanId = props.match?.params.id; 
        axios.get('/scan/'+ scanId,{ headers : {'Authorization' : 'Bearer ' + User.access_token}})
        .then(res => {
            setScan(res.data)
        })
        .catch(err => {
            console.log(err)
        })
    }, [User,props])

    return (
        <TemplatePage>
            <Grid container spacing={1} alignItems="center" direction='column'>
                <Grid item xs={12} sm={12} md={12} lg={12} xl={12} className={classes.container}>
                    <BoxContainer title={Scan?.name}>
                        <BasicInformation ip={Scan?.ip} date={Scan?.date} user={Scan?.user.surname + ' ' + Scan?.user.name} team={Scan?.team.name}/>
                    </BoxContainer>
                </Grid>
                <Grid item xs={12} sm={12} md={12} lg={12} xl={12} className={classes.container} >
                    <Grid container spacing={1} direction='row'>
                        <Grid item xs={12} sm={4} md={3} lg={2} xl={2}>
                            <BoxContainer title='Nmap'>
                                <NmapResult nmap={Scan?.nmap}/>
                            </BoxContainer>
                        </Grid>
                        <Grid item xs={12} sm={8} md={9} lg={10} xl={10}>
                            {Scan.metasploit.map((MetasploitPort, indexMetasploitPort) => (
                                <div key={indexMetasploitPort}>
                                    <Typography color='textSecondary' variant='h6'>{MetasploitPort.port} : </Typography>
                                    {MetasploitPort.modules.map((module, indexModule) => (
                                        <MetasploitResult key={indexModule} metasploit={module}/>
                                    ))}
                                </div>
                            ))}
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </TemplatePage>
    )
}

export default Scan


const initialValuesUser : userApiInterface = {
    surname : '',
    name : '',  
    mail :'',
    job: '',
    ipMsfrpcd : ''
}

const inititalValuesTeam : teamApiInterface = {
    id :'',
    admin :initialValuesUser,
    name : '',
    users :[]
}

const initialValuesScan : ScanApiInterface = {
    id :'',
    name:'',
    ip:'',
    date:'',
    user: initialValuesUser,
    team : inititalValuesTeam,
    metasploit : [],
    nmap : [],
}