import React, { useContext, useState} from 'react';
import { Grid , Button , Typography} from '@material-ui/core'; 
import { Formik , Form } from 'formik';
import {useHistory} from 'react-router-dom';
import * as Yup from 'yup'; 
import axios from 'axios'
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';

import InputField from '../Input/InputField';
import {UserContext} from '../../Context/UserContext';

interface TypeValuesUser {
    surname : string, 
    name : string,
    mail : string,
    job : string,
    ipmsfrpcd : string,
    passwordmsfrpcd : string, 
}

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        containerSubtitle : { 
            borderTop: '1px solid white',
            marginBottom : theme.spacing(1), 
        },
        title: {
            textAlign : 'center', 
            marginTop : theme.spacing(1),
        },
        containerButton : {
            textAlign:'center',
            color : theme.palette.text.primary,
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
        
    })
);



const User = () => {
    const classes = useStyles();
    const history = useHistory();
    const [errorMessage, setErrorMessage] = useState('')
    const {User , setUser} = useContext(UserContext)

    const initialValuesUser : TypeValuesUser = {
        surname : User.surname,
        name : User.name,  
        mail : User.mail,
        job: User.job,
        ipmsfrpcd : User.ipMsfrpcd,
        passwordmsfrpcd : '',
    }

    return (
        <Grid container spacing={1} justify="center" >
            <Formik
                initialValues={initialValuesUser}
                validationSchema={UserSchema}
                validateOnChange={true}
                onSubmit={(values, { setSubmitting , resetForm }) => {
                    axios.post('/user',values,{headers:{'Authorization' : 'Bearer ' + User.access_token}})
                    .then(res => {
                        var data = res.data
                        setUser({
                            ...User,
                            'surname' : data['surname'], 
                            'name' : data['name'],
                            'job' : data['job'], 
                            'ipMsfrpcd' : data['ipMsfrpcd'] 
                        })
                        setErrorMessage('')
                        history.push('/newScan')
                    }).catch(err => {
                        setErrorMessage('An error occured during the modification')
                    });
                    resetForm({})
                    setSubmitting(false)
                }}
            >{({isSubmitting, errors, touched, isValid }) => (
                <Grid item xs={12} sm={8} md={8} lg={8} xl={8}>
                    <Form>
                        <InputField name='surname' label='Surname' color='primary' touched={touched?.surname} error={errors?.surname}  /> 
                        <InputField name='name' label='Name' color='primary' touched={touched?.name} error={errors?.name} /> 
                        <InputField name='job' label='Job' color='primary' type='job' touched={touched?.job} error={errors?.job}/>
                        <div className={classes.containerSubtitle}>
                            <Typography color='textSecondary' className={classes.title} variant='body1'>Sever MSFRPCD</Typography>
                        </div>
                        <InputField name='ipmsfrpcd' label='IP' color='primary' type='mail' touched={touched?.ipmsfrpcd} error={errors?.ipmsfrpcd}/>
                        <InputField name='passwordmsfrpcd' label='Password' color='primary' type='password' touched={touched?.passwordmsfrpcd} error={errors?.passwordmsfrpcd}/>
                        <div className={classes.containerButton}>
                            <Button variant="contained" color='primary' size='large' className={classes.myButton} type='submit' disabled={isSubmitting || !isValid} >Edit</Button>
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

export default User


const surnameRegex = /^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$/
const nameRegex =/^[a-zA-ZáàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\- ]+$/
const textRegex = /^[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ.\- ]+$/
const IpRegex = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/

const UserSchema = Yup.object().shape({
    surname: Yup.string().min(2, 'Too short !').max(20, 'Too Long !').required('Required !').matches(surnameRegex,'Invalid Surname'),
    name : Yup.string().min(2, 'Too short !').max(20, 'Too Long !').required('Required !').matches(nameRegex,'Invalid Name'),
    job: Yup.string().min(2, 'Too short !').max(50, 'Too Long !').required('Required !').matches(textRegex,'Invalid Job'),
    ipmsfrpcd : Yup.string().min(2, 'Too short !').max(50, 'Too Long !').required('Required !').matches(IpRegex,'Invalid IP'),
    passwordmsfrpcd : Yup.string().min(2, 'Too short !').max(50, 'Too Long !').required('Required !'),
});


