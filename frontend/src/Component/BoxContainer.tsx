import React, { ReactNode } from 'react';
import {Paper, Typography} from '@material-ui/core';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';

interface BoxContainerProps {
    title : string | undefined,
    children : ReactNode
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        container : {
            marginTop : theme.spacing(2), 
            marginBottom: theme.spacing(2),
            backgroundColor : theme.palette.background.default
        },
        containerTitle : {
            paddingTop: theme.spacing(1),
            paddingBottom : theme.spacing(1),
            backgroundColor : theme.palette.primary.main
        },
        title : {
            paddingLeft : theme.spacing(2)
        },
        containerContent : {
            paddingTop: theme.spacing(4), 
            paddingBottom : theme.spacing(1),
        }
    })
);


const BoxContainer = (props : BoxContainerProps) => {
    const classes = useStyles();
    return (
        <Paper elevation={3} className={classes.container}>
            <div className={classes.containerTitle}>    
                <Typography color='textSecondary' variant='h6' className={classes.title} >{props.title}</Typography>
            </div>
            <div className={classes.containerContent}>
                {props.children}
            </div>
        </Paper>
    )
}

export default BoxContainer
