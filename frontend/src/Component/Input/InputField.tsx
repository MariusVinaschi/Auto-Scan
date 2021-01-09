import React from 'react'; 
import {Field , ErrorMessage} from "formik";
import TextField from "@material-ui/core/TextField";
import ContainerInput from './ContainerInput'

interface InputFieldProps {
    label:string,
    name:string,
    color?: 'primary' | 'secondary' 
    type?:string,
    touched?:boolean | undefined,
    error?:string | undefined
    disabled?: boolean
}

const InputField = (props:InputFieldProps) => {
    return (
        <ContainerInput>
            <Field 
                color={props.color}
                autoComplete="off"
                variant='outlined'
                label={props.label}
                name={props.name}
                type={props.type || 'text'}
                fullWidth
                disabled={props.disabled}
                as={TextField}
                error={Boolean(props.touched && props.error)}
                helperText={<ErrorMessage name={props.name} />}
            />
        </ContainerInput>
    )
}

export default InputField
