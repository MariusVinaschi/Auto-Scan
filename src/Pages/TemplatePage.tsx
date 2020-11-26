import React, { ReactNode , useState} from 'react'; 
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';

import Header from '../Component/Header';
import Sidebar from '../Component/Sidebar';

interface TemplatePageProps {
    children?:ReactNode
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
    },
    content : (sidebarWidth : number) => ({
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        marginLeft: sidebarWidth + theme.spacing(1),
        margin : theme.spacing(1), 
    }),

  }),
);

const TemplatePage = (props : TemplatePageProps) => {
    const width = 200 ; 
    const [SidebarOpen, setSidebarOpen] = useState(true); 
    const [SidebarWidth , setSidebarWidth] = useState(width);
    const classes = useStyles(SidebarWidth);

    const HideShowSidebar = () => {
        setSidebarOpen(!SidebarOpen)
        if (SidebarWidth === width) {
            setSidebarWidth(0)
        }else {
            setSidebarWidth(width)
        }
    }

    return (
        <div className={classes.root}>
            <Header HideOpenSidebar={HideShowSidebar} isOpen={SidebarOpen} sidebarWidth={SidebarWidth} /> 
            <Sidebar sidebarWidth={SidebarWidth} isOpen={SidebarOpen}/> 
            <div className={classes.content}>
                {props.children}
            </div>
        </div>
    )
}

export default TemplatePage
