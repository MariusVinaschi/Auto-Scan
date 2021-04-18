import React from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Grid, TableRow,TableCell,Typography} from '@material-ui/core';
import {HostsInterface} from '../../Interface/ApiInterface';

import ContainerTable from './ContainerTable';

interface HostInformationProps {
    host : HostsInterface,
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


const HostInformation = (props : HostInformationProps) => {
    const classes = useStyles();
    const list_header_ports = ["Port Id","Service","Product","Extra Info"]
    const list_header_users = ["ID", "Username", "Fullname" , "Bad Password Count", "Logon Count","is Expire","is Disable"]
    const list_header_shares = ["Name","Authorization","Comment"]

    return (
        <Grid container spacing={1} alignItems="center" direction='column'>
            <Grid item xs={11}sm={11} md={11} lg={11} xl={11}>
                <Grid container spacing={1} alignItems="center" direction='row' justify='space-between'>
                    <Typography color='textSecondary' className={classes.text} variant="h6">Hosname : {props.host.name}</Typography>                
                    <Typography color='textSecondary' className={classes.text} variant="h6">IP : {props.host.IP}</Typography>                
                </Grid>
            </Grid>
            <Grid item xs={11} sm={11} md={11} lg={11} xl={11}>
                <ContainerTable listHeader={list_header_ports} title={'Ports : '}>
                    {props.host.Ports.map((port, index) => (
                        <TableRow key={index}>
                            <TableCell>{port.portid}</TableCell>
                            <TableCell>{port.service}</TableCell>
                            <TableCell>{port.product}</TableCell>
                            <TableCell>{port.extrainfo}</TableCell>
                        </TableRow>
                    ))}
                </ContainerTable>
            </Grid>
            <Grid item xs={11} sm={11} md={11} lg={11} xl={11}>
                <ContainerTable listHeader={list_header_users} title={'Users : '}>
                    {props.host.users.map((user, index) => (
                        <TableRow key={index}>
                            <TableCell>{user.uid}</TableCell>
                            <TableCell>{user.username}</TableCell>
                            <TableCell>{user.fullname}</TableCell>
                            <TableCell>{user.bad_password_count}</TableCell>
                            <TableCell>{user.logon_count}</TableCell>
                            <TableCell>{user.is_expire}</TableCell>
                            <TableCell>{user.is_disable}</TableCell>
                        </TableRow>
                    ))}
                </ContainerTable>
            </Grid>
            <Grid item xs={11} sm={11} md={11} lg={11} xl={11}>
                <ContainerTable listHeader={list_header_shares}  title={'Shares :'}>
                    {props.host.shares.map((share, index) => (
                        <TableRow key={index}>
                            <TableCell>{share.share}</TableCell>
                            <TableCell>{share.privs}</TableCell>
                            <TableCell>{share.comment}</TableCell>
                        </TableRow>
                    ))}
                </ContainerTable>
            </Grid>
        </Grid>
    )
}

export default HostInformation
