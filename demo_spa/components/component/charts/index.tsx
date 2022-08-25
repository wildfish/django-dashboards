import React from "react";
import dynamic from 'next/dynamic'
import {Data} from "plotly.js";
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export const Plotly: React.FC<{value: Data[]}> = ({value}) => (
    <Plot
        data={value.data}
        layout={{autosize: true}}
        useResizeHandler={true}
        style={{minHeight: "300px", height: "100%"}}
    />
)