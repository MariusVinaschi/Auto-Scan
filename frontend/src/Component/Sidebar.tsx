import React from 'react'
import { Drawer , List , ListItem , ListItemText, Typography } from '@material-ui/core'; 
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import {Link} from 'react-router-dom';

interface SidebarProps {
    isOpen : boolean, 
    sidebarWidth : number, 
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    drawer : (props : SidebarProps) => ({
        width: props.sidebarWidth,
        flexShrink: 0,
        backgroundColor : theme.palette.primary.main
    }),
    drawerContent : (props : SidebarProps) => ({
        width: props.sidebarWidth,
    }),
    list :{
        marginTop : theme.spacing(3),
    },
    link : {
        textDecoration: 'none',
        color : theme.palette.text.secondary,
        backgroundColor: theme.palette.secondary.main
    },
    ListItem:{
        backgroundColor:theme.palette.primary.main,
        "&:hover": {
            backgroundColor:theme.palette.primary.main,
        }
    },
    containerText:{
        marginTop : theme.spacing(2),
        textAlign:'center',
    },
  }),
);

interface TypeSidebarLink {
    label : string, 
    path : string,
}

const SidebarLinks : TypeSidebarLink[] = [
    {label:'New Metasploit Scan' , path:'/newScan'},
    {label:'New AD Scan' , path:'/newScanAd'},
    {label:'My Metasploit Scans' , path:'/scans'},
    {label:'My AD Scans',path:'/scansAd'},
    {label:'My Teams' , path:'/teams'},
    {label:'Profile' , path:'/profile'},
]

const Sidebar = (props : SidebarProps) => {
    const classes = useStyles(props);
    return (
        <Drawer variant='persistent' open={props.isOpen} className={classes.drawer}>
            <div className={classes.drawerContent}>
                <div className={classes.containerText}> 
                    <Typography color='textSecondary' variant='body1'>Auto Scan</Typography>
                    <Typography color='textSecondary' variant='body2'>Beta Version</Typography>
                    <Typography color='textSecondary' variant='body2'>2020</Typography>
                </div>
                <List className={classes.list}>
                    {SidebarLinks.map((link, index) => (
                        <Link key={index} to={link.path} className={classes.link}>
                            <ListItem button divider={true} className={classes.ListItem} >
                                <ListItemText inset={true} primary={link.label} color='secondary' />
                            </ListItem> 
                        </Link>
                    ))}
                </List>            
            </div>
        </Drawer>
    )
}

export default Sidebar
