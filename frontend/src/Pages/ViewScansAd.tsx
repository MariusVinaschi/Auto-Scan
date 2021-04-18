import React , {useState , useContext , useEffect} from 'react'; 
import {Grid} from '@material-ui/core';
import axios from 'axios';

import TemplateViewPages from '../Component/View/TemplateViewPages';
import {UserContext} from '../Context/UserContext';
import {ScansAdApiInterface, } from '../Interface/ApiInterface';

import InformationBox from '../Component/View/InformationBox';
import TextContainer from '../Component/TextContainer'

const ViewAdScans = () => {
    const [Scans, setScans] = useState<ScansAdApiInterface[]>([])
    const {User} = useContext(UserContext)

    useEffect(() => {
        axios.get('/scansAd',{ headers : {'Authorization' : 'Bearer ' + User.access_token}})
        .then(res => {
            setScans(res.data)
        })
        .catch(err => {
            console.log(err)
        })
    }, [User])

    return (
        <TemplateViewPages title='My Active Directory Scans'>
            {Scans.map((scan) => (
                <Grid item key={scan.id} xs={12} sm={6} md={4} lg={4} xl={4} >
                    <InformationBox id={scan.id} name={scan.name} path={'scanAd'}>
                        <TextContainer label={'User :'} text={scan.user.surname + ' ' + scan.user.name} />
                        <TextContainer label={'Team :'} text={scan.team.name} />
                        <TextContainer label={'Date :'} text={scan.date.substr(0, 10)}/> 
                        <TextContainer label={'Domain Name :'} text={scan.domain.name} /> 
                    </InformationBox>
                </Grid>
            ))}
        </TemplateViewPages>          
    )
}

export default ViewAdScans
