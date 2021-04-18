import React, { ReactNode } from 'react';
import { makeStyles} from '@material-ui/core/styles';
import {Table, TableBody, TableCell, TableContainer,TableHead,TableRow,Paper} from '@material-ui/core';

const useStyles = makeStyles({
    root:{
        width:'100%'
    },
    container:{
        minWidth:'1400px',
        maxHeight: 440,
    },
    tableHead:{
        backgroundColor:'#D1D0D0',
    }
});
interface TableInformationProps { 
    listHeader: string[];
    children : ReactNode;
}

const TableInformation = (props : TableInformationProps) => {
    const classes = useStyles(); 
    return (
        <div className={classes.root}>
            <TableContainer component={Paper} className={classes.container}> 
                <Table size={'small'}>
                    <TableHead className={classes.tableHead}>
                        <TableRow>
                            {props.listHeader.map((label) => (
                                <TableCell>{label}</TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {props?.children}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    )
}

export default TableInformation
