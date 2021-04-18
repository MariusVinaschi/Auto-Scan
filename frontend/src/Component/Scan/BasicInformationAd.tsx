import React from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Grid , Typography} from '@material-ui/core';


interface BasicInformationProps {
    date : string ,
    user: string , 
    team : string , 
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        container: {
            marginRight : theme.spacing(1),
            marginTop : theme.spacing(1)
        },
        text: {
            marginLeft : theme.spacing(2),
            marginRight : theme.spacing(2)
        }
    })
);

const BasicInformation = (props : BasicInformationProps) => {
    const classes = useStyles();
    const arrayText = ['Date : ' + props.date.substr(0, 10), 'User : ' + props.user, 'Team : ' + props.team]

    return (
        <Grid container spacing={1} alignItems="center" direction='row' justify='space-between'>
            {arrayText.map((text, index) => (
                <Typography color='textSecondary' key={index} className={classes.text} variant="h6">{text}</Typography>                
            ))}
        </Grid>
    )
}

export default BasicInformation
