import React, {ReactNode} from 'react'; 
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {Grid , Typography} from '@material-ui/core'

import TemplatePage from '../../Pages/TemplatePage';

interface TemplateViewPagesProps {
    title:string, 
    children : ReactNode,
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        container : {
            marginBottom: theme.spacing(2)
        },
        containerTitle : {
            marginTop : theme.spacing(1),
            marginBottom : theme.spacing(1), 
            
        },
        title : {
            margin: theme.spacing(2),
            paddingBottom : theme.spacing(2),
            paddingTop:theme.spacing(1),
            textAlign:'center',
            borderBottom: '1px solid white'
        },

    })
);


const TemplateViewPages = (props : TemplateViewPagesProps) => {
    const classes = useStyles();
    return (
        <TemplatePage>
            <Grid container spacing={1} alignItems="center" direction='column'> 
                <Grid item xs={12} sm={8} md={8} lg={8} xl={8} className={classes.containerTitle}>
                    <Typography variant='h5' color='textSecondary' className={classes.title}>{props.title}</Typography>
                </Grid>
                <Grid item xs={12} sm={12} md={12} lg={12} xl={12} className={classes.container}>
                    <Grid container spacing={2} direction='row' justify='space-around'>
                        {props.children}
                    </Grid>
                </Grid>
            </Grid>
        </TemplatePage>
    )
}

export default TemplateViewPages
