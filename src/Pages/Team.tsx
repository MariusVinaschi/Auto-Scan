import React , {useEffect,useState,useContext} from 'react'; 
import axios from 'axios';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import {match} from 'react-router-dom';
import {Grid , Typography} from '@material-ui/core';

import {UserContext} from '../Context/UserContext';
import TemplatePage from './TemplatePage'
import {teamApiInterface} from '../Interface/ApiInterface';
import BoxContainer from '../Component/BoxContainer';
import ProfileContainer from '../Component/Profile/ProfileContainer';

interface ParametersInterface{
    id : string, 
}

interface TeamProps {
    match?:match<ParametersInterface>
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
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
        container : {
            minWidth:'100%'
        }

    })
);


const Team = (props : TeamProps) => {
    const  {User} = useContext(UserContext);
    const classes = useStyles();
    const [Team, setTeam] = useState<teamApiInterface | null>(null)

    useEffect(() => {
        var teamId = props.match?.params.id
        axios.get('/team/'+ teamId,{ headers : {'Authorization' : 'Bearer ' + User.access_token}})
        .then(res => {
            setTeam(res.data)
        })
        .catch(err => {
            console.log(err)
        })
    }, [User , props ])


    return (
        <TemplatePage>
            <Grid container spacing={1} alignItems="center" direction='column'>
                <Grid item xs={12} sm={8} md={8} lg={8} xl={8} className={classes.containerTitle}>
                    <Typography variant='h4' color='textSecondary' className={classes.title}>{Team?.name}</Typography>
                </Grid>
                <Grid item xs={12} sm={12} md={12} lg={12} xl={12} className={classes.container}>
                    <BoxContainer title="Administrators">
                        <Grid container spacing={1} alignItems="center" direction='row' justify='space-around'>
                            <Grid item xs={12} sm={6} md={4} lg={4} xl={4}>
                                <ProfileContainer surname={Team?.admin.surname} name={Team?.admin.name} mail={Team?.admin.mail} job={Team?.admin.job}/>
                            </Grid>
                        </Grid>
                    </BoxContainer>
                </Grid>
                <Grid item xs={12} sm={12} md={12} lg={12} xl={12} className={classes.container} >
                    <BoxContainer title="Users">
                        <Grid container spacing={1} alignItems="center" direction='row' justify='space-around'>
                            {Team?.users.map((user, index) => (
                                <Grid key={index} item xs={12} sm={6} md={4} lg={4} xl={4}>
                                    <ProfileContainer surname={user.surname} name={user.name} mail={user.mail} job={user.job}/>
                                </Grid>
                            ))}
                        </Grid>
                    </BoxContainer>
                </Grid>
            </Grid>
        </TemplatePage>
    )
}

export default Team
