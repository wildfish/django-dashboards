import React from "react";
import 'react-tabulator/lib/styles.css';
import 'react-tabulator/lib/css/tabulator.min.css'
import {ColumnDefinition, ReactTabulator} from 'react-tabulator'

export const Tabulator = ({value}: { value: any }) => {
    /* TODO Would need some custom hooks for the pagination here, MPA is via the request/ajax but we'd need to pass
    *  into gql
    *
    * We probably want to use something else like ReactTable, this was thrown in so MPA and SPA could quickly use the same
    * thing i.e Tabulator, but it's not great.
    * */
    let data = JSON.parse(JSON.stringify(value));
    let rows = data.rows;
    const columns: ColumnDefinition[] = Object.keys(rows[0]).map(k => {return {title: k, field: k}})
    return <ReactTabulator
        data={rows}
        layout="fitColumns"
        columns={columns}
    />

}