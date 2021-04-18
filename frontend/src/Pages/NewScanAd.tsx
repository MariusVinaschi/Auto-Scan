import React , {useEffect , useContext ,useState} from 'react'; 
import {Grid, Typography , Button, CircularProgress , Backdrop} from '@material-ui/core'; 
import { Formik , Form } from 'formik';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import * as Yup from 'yup';
import {useHistory} from 'react-router-dom';
import axios from 'axios';

import TemplatePage from './TemplatePage'; 
import InputField from '../Component/Input/InputField';
import SelectField, {FormikSelectItem} from '../Component/Input/SelectField';
import { UserContext } from '../Context/UserContext';
import {teamApiInterface} from '../Interface/ApiInterface';


interface TypeValuesNewScanAd {
    name : string, 
    ip : string, 
    team : string, 
}

const initialValuesNewScanAd : TypeValuesNewScanAd = {
    name: '', 
    ip : '',
    team : '', 
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        root: {

        },
        container : {
            // backgroundColor:'blue',
        },
        form: {
            padding: theme.spacing(1)
        },
        title : {
            margin: theme.spacing(2),
            paddingBottom : theme.spacing(2),
            paddingTop:theme.spacing(1),
            textAlign:'center',
            color: theme.palette.text.secondary
        },
        containerButton : {
            textAlign:'center',
            marginTop: theme.spacing(3)
        },
        myButton : {
            color:theme.palette.text.secondary,
            backgroundColor:theme.palette.primary.main
        },
        containerError : {
            marginTop:theme.spacing(2),
            textAlign: 'center',
            color : theme.palette.error.dark
        }, 
        backdrop: {
            zIndex: theme.zIndex.drawer + 1,
            color: theme.palette.primary.main,
        }
    })
);


const NewScanAd = () => {
    const classes = useStyles();     
    const {User} = useContext(UserContext)
    const [errorMessage, setErrorMessage] = useState('')
    const [TeamSelect, setTeamSelect] = useState<FormikSelectItem[]>([])
    const history = useHistory();
    const [loading, setLoading] = useState(false)

    const setSelectFieldValue = (teams : teamApiInterface[]) => {
        var arraySelectField: FormikSelectItem[] = []
        teams.forEach(team => {
            arraySelectField.push({label:team['name'] , value : team['id']})
        });
        return arraySelectField
    }

    const createListTarget = (stringIp : string) => {   
        const IpRegex = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/
        var temporary_list_target = stringIp.split(' ');
        var list_target: string[] = [];
        temporary_list_target.forEach( (element) => {
            if ( element !== " " && IpRegex.test(element)){
                list_target.push(element);
            }

        });
        return list_target
    }

    useEffect(() => {
        axios.get('/teams',{ headers : {'Authorization' : 'Bearer ' + User.access_token}})
        .then(res => {
            var arraySelectField = setSelectFieldValue(res.data)
            setTeamSelect(arraySelectField)
        })
        .catch(err => {
            console.log(err)
        })
    }, [User])

    return (
        <TemplatePage>
            <Grid container spacing={1} justify="center"> 
                <Formik
                    initialValues={initialValuesNewScanAd}
                    validationSchema={NewScanAdSchema}
                    validateOnChange={true}
                    onSubmit={(values, { setSubmitting , resetForm }) => {
                        var list_target = createListTarget(values.ip)
                        var data = {
                            "scan_name":values.name,
                            "list_target": list_target,
                            "team":values.team
                        }
                        setLoading(true)
                        axios.post('/newScanAd',data,{headers:{'Authorization': 'Bearer '+ User.access_token}})
                        .then(res => {
                            setLoading(false)
                            setErrorMessage('')
                            history.push('/scanAd/'+res.data.scanId)
                        })
                        .catch(err => {
                            setLoading(false)
                            setErrorMessage(err.response.data.message)
                        })
                        resetForm({})
                        setSubmitting(false)
                    }}
                >{({isSubmitting, errors, touched, isValid }) => (
                    <Grid item xs={12} sm={8} md={8} lg={8} xl={8} className={classes.container}>
                        <Form className={classes.form}>
                            <Typography variant='h6' className={classes.title}>Launch Active Directory Scan</Typography>
                            <InputField label={'Name'} name={'name'} color='primary' error={errors?.name} touched={touched?.name} /> 
                            <InputField label={'List of Target'} name={'ip'} color='primary' error={errors?.ip} touched={touched?.ip}  />
                            <SelectField items={TeamSelect} label={'Team'} name={'team'} error={errors?.team} touched={touched?.team} />
                            <div className={classes.containerButton}>
                                <Button variant="contained" size='large' color='primary' className={classes.myButton} type='submit' disabled={isSubmitting || !isValid} >Launch</Button>
                            </div>
                            <div className={classes.containerError}> 
                                <Typography variant='body1'>{errorMessage}</Typography>
                            </div>
                            {loading && <Backdrop className={classes.backdrop} open={loading}><CircularProgress color="inherit" /></Backdrop>}
                        </Form>
                    </Grid>
                )}
                </Formik>
            </Grid>
        </TemplatePage>
    )
}

export default NewScanAd

const NameRegex = /^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$/

const NewScanAdSchema = Yup.object().shape({
    name: Yup.string().required('Required !').min(2, 'Too short !').max(50, 'Too Long !').matches(NameRegex,'Invalid Name'),
    ip : Yup.string().required('Required !'),
    team : Yup.string().required('Required !').min(2, 'Too short !').max(50, 'Too Long !'),
});
