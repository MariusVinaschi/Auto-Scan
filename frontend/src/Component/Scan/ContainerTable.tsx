import React, { ReactNode } from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Typography} from '@material-ui/core';
import {DomainInterface} from '../../Interface/ApiInterface';

import TableInformation from './TableInformation';

interface BasicInformationProps {
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
        },
        containerTitle : {
            padding : theme.spacing(1),
            backgroundColor: theme.palette.primary.main,
        },
        myTitle: { 
            color: theme.palette.text.secondary, 
            textAlign:'center'
        },
    })
);

interface ContainerTableProps { 
    title : string,
    listHeader: string[];
    children : ReactNode;
}

const ContainerTable = (props : ContainerTableProps) => {
    const classes = useStyles();

    return (
        <div className={classes.container}>
            <div className={classes.containerTitle}>
                <Typography color='textSecondary'className={classes.myTitle} variant='h5'>{props.title}</Typography>
            </div>
            <TableInformation listHeader={props.listHeader}> 
                {props?.children}
            </TableInformation>
        </div>
    )
}

export default ContainerTable
