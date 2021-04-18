import React from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Grid, TableRow,TableCell,Typography} from '@material-ui/core';
import {DomainInterface} from '../../Interface/ApiInterface';

import ContainerTable from './ContainerTable';

interface DomainInformationProps {
    domain : DomainInterface,
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


const DomainInformation = (props : DomainInformationProps) => {
    const classes = useStyles();
    const list_header_services = ["Service Name","Name","Member of","Password Last Set","Last Logon"]
    const list_header_users = ["Username", "Password", "Mail" , "Password Last Set", "Last Logon"]
    const list_header_groups = ["Index","Name"]

    return (
        <Grid container spacing={1} alignItems="center" direction='column'>
            <Grid item xs={11}sm={11} md={11} lg={11} xl={11}>
                <Grid container spacing={1} alignItems="center" direction='row' justify='space-between'>
                    <Typography color='textSecondary' className={classes.text} variant="h6">Domain Controller Name : {props.domain.domain_controler_name}</Typography>                
                    <Typography color='textSecondary' className={classes.text} variant="h6">Domain Controller IP : {props.domain.domain_controler_ip}</Typography>                
                </Grid>
            </Grid>
            <Grid item xs={11} sm={11} md={11} lg={11} xl={11}>
                <ContainerTable listHeader={list_header_users} title={'Users : '}>
                    {props.domain.users.map((user, index) => (
                        <TableRow key={index}>
                            <TableCell>{user.username}</TableCell>
                            <TableCell>{user.password}</TableCell>
                            <TableCell>{user.mail}</TableCell>
                            <TableCell>{user.last_logon}</TableCell>
                            <TableCell>{user.password_last_set}</TableCell>
                        </TableRow>
                    ))}
                </ContainerTable>
            </Grid>
            <Grid item xs={11} sm={11} md={11} lg={11} xl={11}>
                <ContainerTable listHeader={list_header_groups} title={'Groups : '}>
                    {props.domain.groups.map((group, index) => (
                        <TableRow key={index}>
                            <TableCell>{index}</TableCell>
                            <TableCell>{group.name}</TableCell>
                        </TableRow>
                    ))}
                </ContainerTable>
            </Grid>
            <Grid item xs={11} sm={11} md={11} lg={11} xl={11}>
                <ContainerTable listHeader={list_header_services}  title={'Services :'}>
                    {props.domain.services.map((service, index) => (
                        <TableRow key={index}>
                            <TableCell>{service.service_principal_name}</TableCell>
                            <TableCell>{service.name}</TableCell>
                            <TableCell>{service.member_of}</TableCell>
                            <TableCell>{service.password_last_set}</TableCell>
                            <TableCell>{service.last_logon}</TableCell>
                        </TableRow>
                    ))}
                </ContainerTable>
            </Grid>
        </Grid>
    )
}

export default DomainInformation
