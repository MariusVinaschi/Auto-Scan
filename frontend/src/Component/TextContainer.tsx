import React from 'react'; 
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';

interface TextContainerProps {
    label : string | undefined, 
    text : string | undefined,
}


const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    containerInformation:{
        paddingLeft : theme.spacing(1),
        paddingRight : theme.spacing(1)
    },
    textContainer:{
        textAlign:'center'
    },
  }),
);


const TextContainer = (props : TextContainerProps) => {
    const classes = useStyles();
    return (
        <div className={classes.containerInformation}>
            <div>
                <Typography color='textSecondary' variant='h6' >{props.label}</Typography>
            </div>
            <div className={classes.textContainer}>
                <Typography color='textSecondary' variant='body1'>{props.text}</Typography>
            </div>
        </div>
    )
}

export default TextContainer
