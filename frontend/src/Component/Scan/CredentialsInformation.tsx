import React from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import { TableCell, TableContainer,TableHead,TableRow} from '@material-ui/core';
import {CredentialsInterface} from '../../Interface/ApiInterface';
import TableInformation from '../Scan/TableInformation';


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

interface CredentialResultProps {
    listCredentials : CredentialsInterface[],
}


const CredentialResult = (props : CredentialResultProps) => {
    const classes = useStyles(); 
    const listHeader : string[] = ['IP','Domain Name' ,'Username','Password']
    return (
        <TableInformation ListHeader={listHeader}>
            {props.listCredentials.map((creds, index) => (
                <TableRow key={index}>
                    <TableCell align="center">{creds.ip}</TableCell>
                    <TableCell align="center">{creds.domain}</TableCell>
                    <TableCell align="center">{creds.username}</TableCell>
                    <TableCell align="center">{creds.password}</TableCell>
                </TableRow>
            ))}
        </TableInformation>
    )
}

export default CredentialResult
