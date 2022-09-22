import React from "react";
import dynamic from 'next/dynamic'
import {Value} from "@/types";
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export const Plotly: React.FC<{value: Value}> = ({value}) => {
    return <Plot
        data={JSON.parse(JSON.stringify(value.data))}
        layout={{autosize: true}}
        useResizeHandler={true}
        style={{minHeight: "300px", height: "100%"}}
    />
}