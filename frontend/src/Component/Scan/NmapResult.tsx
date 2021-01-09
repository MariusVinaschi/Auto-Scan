import React from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {List, ListItem, ListItemText} from '@material-ui/core';
import {NmapInterface} from '../../Interface/ApiInterface';


const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        root :{
            minHeight : '60vh', 
            maxHeight:'60vh',
            overflowY: 'scroll'
        },
        ListItem:{
            color: theme.palette.text.secondary
        }

    })
);

interface NmapResultProps {
    nmap : NmapInterface[]
}


const NmapResult = (props : NmapResultProps) => {
    const classes = useStyles(); 
    return (
        <List className={classes.root}>
            {props.nmap.map((port, index) => (
                <ListItem key={index} divider={true} className={classes.ListItem} >
                    <ListItemText inset={true} primary={port.port+' '+ port.service}/>
                </ListItem> 
            ))}
        </List>
    )
}

export default NmapResult
