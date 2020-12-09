import React from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Typography} from '@material-ui/core'; 

import TextContainer from '../TextContainer';

interface ProfileContainerProps {
    surname : string | undefined,
    name : string | undefined, 
    mail : string | undefined, 
    job : string | undefined , 
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        container :{
            minWidth:'200px',
            border : '1px solid white',
            marginBottom : theme.spacing(2),
            marginTop : theme.spacing(1)
        },
        containerTitle : {
            paddingTop: theme.spacing(1),
            paddingBottom : theme.spacing(1),
            backgroundColor : theme.palette.primary.main,
            borderBottom : '1px solid white',
            textAlign : "center"
        },
        containerContent : {
            padding : theme.spacing(1)
        }   
    })
);

const ProfileContainer = (props :  ProfileContainerProps) => {
    const classes = useStyles();
    return (
        <div className={classes.container}>
            <div className={classes.containerTitle}>
                <Typography color='textSecondary' variant='h5'>{props.surname} {props.name}</Typography>
            </div>
            <div className={classes.containerContent}>
                <TextContainer label='Mail :' text={props.mail}/>
                <TextContainer label='Job :' text={props.job}/>
            </div>
        </div>
    )
}

export default ProfileContainer
