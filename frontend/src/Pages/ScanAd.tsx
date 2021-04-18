import React , {useEffect , useContext, useState} from 'react'; 
import axios from 'axios';
import {match} from 'react-router-dom';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Grid } from '@material-ui/core';

import {UserContext} from '../Context/UserContext';
import TemplatePage from './TemplatePage';
import {ScanAdApiInterface , userApiInterface , teamApiInterface, DomainInterface} from '../Interface/ApiInterface';
import BoxContainer from '../Component/BoxContainer';
import BasicInformationAd from '../Component/Scan/BasicInformationAd';

import DomainInformation from '../Component/Scan/DomainInformation';
import HostInformation from '../Component/Scan/HostInformation';

interface ParametersInterface{
    id : string, 
}

interface ScanAdProps {
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
            minWidth:'100%',
            textAlign :'center',
        }, 
        portTitle : {
            textDecoration: 'underline'
        },
        containerTable :{
            textAlign:'center',
        }

    })
);

const ScanAd = (props : ScanAdProps) => {
    const {User} = useContext(UserContext)    
    const [Scan, setScan] = useState<ScanAdApiInterface>(initialValuesScanAd)
    const classes = useStyles();

    useEffect(() => {
        var scanId = props.match?.params.id; 
        axios.get('/scanAd/'+ scanId,{ headers : {'Authorization' : 'Bearer ' + User.access_token}})
        .then(res => {
            console.log(res.data)
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
                        <BasicInformationAd date={Scan?.date} user={Scan?.user.surname + ' ' + Scan?.user.name} team={Scan?.team.name}/>
                    </BoxContainer>
                </Grid>
                <Grid item xs={12} sm={12} md={12} lg={12} xl={12} className={classes.container} >
                    <BoxContainer title={"Domain Name : " + Scan?.domain?.name}>
                        <DomainInformation domain={Scan?.domain}/>
                    </BoxContainer>
                </Grid>
                {Scan.hosts.map((host, index) => (
                    <Grid item xs={12} sm={12} md={12} lg={12} xl={12} className={classes.container} key={index}>
                        <BoxContainer title={host?.name}>
                            <HostInformation host={host}/>                                                                                          
                        </BoxContainer>
                    </Grid>
                ))}
            </Grid>
        </TemplatePage>
    )
}

export default ScanAd


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

const initialValuesDomain : DomainInterface = {
    name : "",
    domain_controler_ip : "",
    domain_controler_name : "",
    users : [],
    groups : [],
    services : []
}

const initialValuesScanAd : ScanAdApiInterface = {
    id :'',
    name:'',
    list_target:[],
    user: initialValuesUser,
    team : inititalValuesTeam,
    date:'',
    hosts : [],
    domain : initialValuesDomain,
    credentials : []
}

