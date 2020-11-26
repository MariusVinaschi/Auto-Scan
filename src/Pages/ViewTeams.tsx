import React , {useState , useContext , useEffect} from 'react'; 
import {Grid} from '@material-ui/core';
import axios from 'axios';

import TemplateViewPages from '../Component/View/TemplateViewPages';
import {UserContext} from '../Context/UserContext';
import {teamApiInterface , userApiInterface} from '../Interface/ApiInterface';
import InformationBox from '../Component/View/InformationBox';
import TextContainer from '../Component/TextContainer';

const ViewTeams = () => {
    const [Teams, setTeams] = useState<teamApiInterface[]>([])
    const {User} = useContext(UserContext);

    useEffect(() => {
        axios.get('/teams',{ headers : {'Authorization' : 'Bearer ' + User.access_token}})
        .then(res => {
           setTeams(res.data )
        })
        .catch(err => {
            console.log(err)
        })
    }, [User])

    const setUsers = (arrayUsers : userApiInterface[]) => {
        var stringUsers:string = ''
        arrayUsers.forEach(user  => {
            stringUsers += user.surname + ' '+ user.name + ','
        });
        return stringUsers
    }

    return (
        <TemplateViewPages title='My Teams'>
            {Teams.map((team) => (
                <Grid item key={team.id} xs={12} sm={6} md={4} lg={4} xl={4}>
                    <InformationBox id={team.id} name={team.name} path={'team'}>
                        <TextContainer label={'Admin :'} text={team.admin.surname +' '+ team.admin.name} />
                        <TextContainer label={'Users :'} text={setUsers(team.users)} />
                    </InformationBox>
                </Grid>
            ))}
        </TemplateViewPages>   
    )
}

export default ViewTeams
