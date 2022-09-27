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
        const choices = element.choices.map((choice) => <option value={choice[0]}>{choice[1]}</option>)
        return <select id={element.id} name={element.name} value={element.value} onChange={onChange}>
            {choices}
        </select>

    } else if (element.field_type === 'Textarea') {
        return <textarea name={element.name} id={element.id} onChange={onChange}>{element.value}</textarea>
    } else {
        return <input type={"text"} id={element.id} name={element.name} value={element.value} onChange={onChange} />
    }
}

export const Form = ({value}: { value: Value }) => {
    const [filter, setFilter] = useContext(FilterContext)
    const data = JSON.parse(JSON.stringify(value))
    const method = data.method

    const onChange = event => {
        setFilter(filter => ({ ...filter, [event.target.name]: event.target.value }))
    }

    const onSubmit = event => {
        event.preventDefault()
    }

    return (
        <form method={method} onSubmit={onSubmit}>
            {data.form.map((field: Field) => (
                <p key={field.id}>
                    <label>
                        {field.label}
                        <FormFieldComponent element={field} onChange={onChange}/>
                        {field.help_text != "" && <div>{field.help_text}</div>}
                    </label>
                </p>
            ))}
        </form>
    )
}
