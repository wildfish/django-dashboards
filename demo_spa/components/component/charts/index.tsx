import React from "react";
import dynamic from 'next/dynamic'
import {Value, DataValue} from "@/types";
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export const Plotly = ({value}: {value: Value}) => {
    return <Plot
        data={JSON.parse(JSON.stringify((value as DataValue).data))}
        layout={{autosize: true}}
        useResizeHandler={true}
        style={{minHeight: "300px", height: "100%"}}
    />
}