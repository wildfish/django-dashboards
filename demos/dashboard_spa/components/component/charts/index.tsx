import React from "react";
import dynamic from 'next/dynamic'
import {Value, DataValue} from "@/types";
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export const Plotly = ({value}: {value: Value}) => {
    try {
        return <Plot
            data={JSON.parse(value).data}
            layout={{autosize: true}}
            useResizeHandler={true}
            style={{minHeight: "300px", height: "100%"}}
        />
    } catch (err) {
        console.log("error", err)
        console.log(value)
        return
    }
}