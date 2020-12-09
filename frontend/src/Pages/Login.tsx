import React , {useState , useContext} from 'react'; 
import {Grid, Typography , Button} from '@material-ui/core'; 
import {useHistory} from 'react-router-dom'
import { Formik , Form } from 'formik';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import * as Yup from 'yup';
import axios from 'axios';

import InputField from '../Component/Input/InputField';
import {UserContext , UserInterface} from '../Context/UserContext';

interface TypeValuesLogin {
    mail : string, 
    password : string
}

const initialValuesLogin : TypeValuesLogin = {
    mail : '', 
    password : '',
}


const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        primaryTitle: {
            textAlign:'center',
            marginTop:theme.spacing(10),
            color:theme.palette.text.primary
        },
        secondaryTitle : {
            textAlign:'center',
            marginTop:theme.spacing(5),
            color:theme.palette.text.secondary
        },
        containerInput : {
            marginTop : theme.spacing(2)
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
        }
    })
);


const Login = () => {
    const [errorMessage, setErrorMessage] = useState('')
    const history = useHistory();
    const classes = useStyles();     
    const {setUser} = useContext(UserContext)

    const updateContext = (data : UserInterface) => {
        var newUser = {
            'access_token' : data.access_token, 
            'surname' : data.surname, 
            'name' : data.name,
            'mail' : data.mail, 
            'job' : data.job, 
            'ipMsfrpcd' : data.ipMsfrpcd
        }
        setUser(newUser)
    }

    return (
        <Grid container justify="center"> 
            <Formik
                initialValues={initialValuesLogin}
                validationSchema={LoginSchema}
                validateOnChange={true}
                onSubmit={(values, { setSubmitting , resetForm }) => {
                    axios.post('/login',values)
                    .then(res => {
                        updateContext(res.data)
                        setErrorMessage('')
                        history.push('/newScan')
                    })
                    .catch(err => {
                        setErrorMessage(err.response.data.message)
                    })
                    resetForm({})
                    setSubmitting(false)
                }}
            >{({isSubmitting, errors, touched, isValid }) => (
                <Grid item xs={12} sm={8} md={6} lg={6} xl={6} >
                    <Form>
                        <Typography variant={'h3'} className={classes.primaryTitle}>Auto Scan</Typography>
                        <Typography variant={'h5'} className={classes.secondaryTitle}>Sign In</Typography>
                        <div className={classes.containerInput}>
                            <InputField label='Mail' name='mail' color='primary' type='mail' touched={touched?.mail} error={errors?.mail}/>
                            <InputField label='Password' name='password' color='primary' type='password' touched={touched?.password} error={errors?.password} />
                        </div>
                        <div className={classes.containerButton}>
                            <Button variant="contained" color='primary' size='large' className={classes.myButton} type='submit' disabled={isSubmitting || !isValid} >Login</Button>
                        </div>
                        <div className={classes.containerError}> 
                            <Typography variant='body1'>{errorMessage}</Typography>
                        </div>
                    </Form>
                </Grid>
            )}
            </Formik>
        </Grid>
    )
}

export default Login


const LoginSchema = Yup.object().shape({
    mail : Yup.string().email('Invalid Email').min(2, 'Too short !').max(50, 'Too Long !').required('Required !'),
    password : Yup.string().required('Required !'),
});