import React , {useState , useContext , useEffect} from 'react'; 
import {Grid} from '@material-ui/core';
import axios from 'axios';

import TemplateViewPages from '../Component/View/TemplateViewPages';
import {UserContext} from '../Context/UserContext';
import {ScansApiInterface , NmapInterface} from '../Interface/ApiInterface';

import InformationBox from '../Component/View/InformationBox';
import TextContainer from '../Component/TextContainer'

const ViewScans = () => {
    const [Scans, setScans] = useState<ScansApiInterface[]>([])
    const {User} = useContext(UserContext)

    useEffect(() => {
        axios.get('/scans',{ headers : {'Authorization' : 'Bearer ' + User.access_token}})
        .then(res => {
            setScans(res.data)
        })
        .catch(err => {
            console.log(err)
        })
    }, [User])

    const setPorts = (ports: NmapInterface[] ) => {
        var stringPort:string = ''
        ports.forEach(port  => {
            stringPort += port.port + ', '
        });
        return stringPort
    }

    return (
        <TemplateViewPages title='My Scans'>
            {Scans.map((scan) => (
                <Grid item key={scan.id} xs={12} sm={6} md={4} lg={4} xl={4} >
                    <InformationBox id={scan.id} name={scan.name} path={'scan'}>
                        <TextContainer label={'User :'} text={scan.user.surname + ' ' + scan.user.name} />
                        <TextContainer label={'Team :'} text={scan.team.name} />
                        <TextContainer label={'Date :'} text={scan.date.substr(0, 10)}/> 
                        <TextContainer label={'Ports :'} text={setPorts(scan.nmap)}/> 
                    </InformationBox>
                </Grid>
            ))}
        </TemplateViewPages>          
    )
}

export default ViewScans
