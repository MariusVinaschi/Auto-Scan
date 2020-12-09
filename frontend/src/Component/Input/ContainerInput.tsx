import React, { ReactNode } from 'react';
import { makeStyles, createStyles, Theme} from '@material-ui/core/styles';

interface ContainerInputProps {
    children: ReactNode
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        containerInput:{
            margin:'10px 0 10px 0',
        }
    })
);



const ContainerInput = (props:ContainerInputProps) => {
    const classes = useStyles();
    return (
        <div className={classes.containerInput}>
            {props.children}
        </div>
    )
}

export default ContainerInput
