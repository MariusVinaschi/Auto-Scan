import React from 'react'; 
import BoxContainer from '../BoxContainer';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';

import {ModuleInterface} from '../../Interface/ApiInterface';

interface MetasploitResultProps {
    metasploit : ModuleInterface,
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    text: {

    }
  }),
);

const MetasploitResult = (props : MetasploitResultProps) => {
    const classes = useStyles();
    
    return (
        <BoxContainer title={props.metasploit.name}>
            {props.metasploit.results.map((text, index) => (
                <Typography color='textSecondary' variant='body1' className={classes.text} key={index} >{text}</Typography>
            ))}
        </BoxContainer>
    )
}

export default MetasploitResult
