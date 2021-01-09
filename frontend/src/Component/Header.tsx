import React , {useContext} from 'react';
import {AppBar , Toolbar , Typography, IconButton, Hidden } from '@material-ui/core';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';

import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';

import {UserContext} from '../Context/UserContext';

interface HeaderProps {
    HideOpenSidebar: () => void, 
    isOpen: Boolean,
    sidebarWidth : number , 
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: (props: HeaderProps) => ({
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        marginLeft: props.sidebarWidth,
    }),
    grow: {
        flexGrow :1,
    },
    containerIcon: {
        marginRight: theme.spacing(1), 
    },
    title : {},
    containerUser :{
        display:'flex', 
        flexDirection:'row',
        marginLeft: theme.spacing(1), 
        paddingLeft:theme.spacing(1),
        paddingRight : theme.spacing(1),
         
    }, 
    avatar:{
        width: theme.spacing(5),
        height: theme.spacing(5),
    },
    user: {
        paddingLeft:theme.spacing(1), 
        display:'flex',
        alignItems:'center'
    }
  }),
);

const Header = (props : HeaderProps) => {
    const classes = useStyles(props);
    const {User} = useContext(UserContext)

    return (
        <div className={classes.root}>
            <AppBar position='static'>
                <Toolbar>
                    <IconButton edge='start' color='inherit' className={classes.containerIcon} onClick={() => props.HideOpenSidebar()}>
                        {props.isOpen ? <ChevronLeftIcon /> : <MenuIcon/>}
                    </IconButton>
                    <Typography className={classes.title} variant="h6">Auto Scan</Typography>
                    <div className={classes.grow} />
                    <div className={classes.containerUser}>
                        <AccountCircleIcon fontSize="large"  />
                        <Hidden xsDown> 
                            <Typography className={classes.user} variant="h6">{User.name + " " + User.surname}</Typography>
                        </Hidden>
                    </div>
                </Toolbar>
            </AppBar>
        </div>
    )
}

export default Header
