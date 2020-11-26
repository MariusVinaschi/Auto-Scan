import React , {ReactNode} from 'react';
import {useHistory} from 'react-router-dom';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { Paper, Typography, Button } from '@material-ui/core';

interface InformationBoxProps {
    name: string , 
    path : string, 
    id: string, 
    children?: ReactNode
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root:{
        backgroundColor : theme.palette.background.default,
        minWidth: '250px'
    },
    containerTitle : {
        padding : theme.spacing(1),
        backgroundColor: theme.palette.primary.main,
    },
    myTitle: { 
        color: theme.palette.text.secondary, 
        textAlign:'center'
    },
    containerContent :{ 
        padding : theme.spacing(1)
    },
    containerButton : {
        textAlign:'center',
        color : theme.palette.text.primary,
        marginTop: theme.spacing(3)
    },
    myButton : {
        color:theme.palette.text.secondary,
        backgroundColor:theme.palette.primary.main,
        marginTop: theme.spacing(1),
        marginBottom : theme.spacing(1)
    },
  }),
);

const InformationBox = (props : InformationBoxProps) => {
    const classes = useStyles();
    const history = useHistory();
    return (
        <Paper elevation={3} className={classes.root}>
            <div className={classes.containerTitle}>
                <Typography color='textSecondary'className={classes.myTitle} variant='h5'>{props.name}</Typography>
            </div>
            <div className={classes.containerContent}>
                {props.children}
            </div>
            <div className={classes.containerButton}>
                <Button variant="contained" color='primary' size='large' className={classes.myButton} onClick={() => history.push(props.path + '/' + props.id) } >View</Button>
            </div>
        </Paper>
    )
}

export default InformationBox
