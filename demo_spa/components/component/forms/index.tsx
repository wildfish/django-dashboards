import React, {useContext} from "react";
import {
    Value,
} from "@/types";
import {FilterContext} from "../../../appContext";

type Field = {
    name: string
    label: string
    value: string
    help_text: string
    id: string
    field_type: string
    required: boolean
    choices: string[]
}

type FormFieldComponentProps = {
    element: Field
    onChange: any
}

const FormFieldComponent = ({element, onChange} : FormFieldComponentProps) => {
    if (element.field_type === 'Select') {
        const choices = element.choices.map((choice) => <option value={choice[0]} key={choice[0]}>{choice[1]}</option>)
        return <select id={element.id} name={element.name} defaultValue={element.value} onChange={onChange}>
            {choices}
        </select>

    } else if (element.field_type === 'Textarea') {
        return <textarea name={element.name} id={element.id} onChange={onChange} defaultValue={element.value} />
    } else {
        return <input type={"text"} id={element.id} name={element.name} defaultValue={element.value} onChange={onChange} />
    }
}

type FormProps = {
    component: any
    value: Value
}

export const Form = ({component, value}: FormProps) => {
    const componentKey = component.key
    const [filters, setFilter] = useContext(FilterContext)
    const data = JSON.parse(JSON.stringify(value))
    const method = data.method
    const dependents = data.dependents

    const onChange = event => {
        const newFilters = [...dependents, componentKey].reduce((a, b) => {
            a[b] = {...a[b], [event.target.name]: event.target.value}
            return a
        }, {...filters})
        // update the filters for the depentent components
        setFilter(newFilters)
    }

    const onSubmit = event => {
        event.preventDefault()
        // todo: handle form submit here
    }

    return (
        <form method={method} onSubmit={onSubmit}>
            {data.form.map((field: Field) => (
                <p key={field.id}>
                    <label>
                        {field.label}:
                        <FormFieldComponent element={field} onChange={onChange}/>
                        {field.help_text != "" && <div>{field.help_text}</div>}
                    </label>
                </p>
            ))}
        </form>
    )
}
