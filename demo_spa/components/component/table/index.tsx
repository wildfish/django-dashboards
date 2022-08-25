import React from "react";
import 'react-tabulator/lib/styles.css';
import 'react-tabulator/lib/css/tabulator.min.css'
import {ColumnDefinition, ReactTabulator} from 'react-tabulator'

export const Tabulator: React.FC<{ value: any }> = ({value}) => {
    /* TODO Would need some custom hooks for the pagination here, MPA is via the request/ajax but we'd need to pass
    *  into gql
    *
    * autoLayout doesn't seem to work and we need columns so copy and define from fields otherwise it crashes out,
    * likely we'd want to pass this in, or even from the component itself in gql
    * */
    let data = JSON.parse(JSON.stringify(value))
    let rows = data.rows;
    const columns: ColumnDefinition[] = Object.keys(rows[0]).map(k => {return {title: k, field: k}})
    return <ReactTabulator
        data={rows}
        layout="fitColumns"
        columns={columns}
    />

}