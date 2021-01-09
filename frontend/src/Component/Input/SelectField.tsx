import React from 'react';
import {Field , ErrorMessage } from "formik";
import {MenuItem , FormControl , InputLabel , Select , FormHelperText} from "@material-ui/core";
import ContainerInput from '../Input/ContainerInput';

export interface FormikSelectItem {
    label: string;
    value: string;
}

interface SelectFieldProps {
    label : string,
    name : string, 
    items: Array<FormikSelectItem>,
    error?:string | undefined,
    touched? : boolean | undefined,
}

const SelectField = (props : SelectFieldProps) => {
    return (
        <ContainerInput>
            <FormControl fullWidth variant='outlined' error={Boolean(props.touched && props.error)}>
                <InputLabel>{props.label}</InputLabel>
                <Field name={props.name} as={Select} type='Select' label={props.label} >
                    {props.items.map((item,key) =>
                        <MenuItem key={key} value={item.value} color={'primary'}>
                            {item.label}
                        </MenuItem>
                    )}
                </Field>
                <FormHelperText>{<ErrorMessage name={props.name} />}</FormHelperText>
            </FormControl>
        </ContainerInput>
    )
}

export default SelectField
