import React from "react";
import dynamic from 'next/dynamic'
import {Value} from "@/types";
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export const Plotly: React.FC<{value: Value}> = ({value}) => {
    // TODO not sure why some charts work but others don't unless we do this weird parse/unparse, the types are the same
    // if I save data above as a const it works, but not inside this component, the chart fails to render?
    return <Plot
        data={JSON.parse(JSON.stringify(value.data))}
        layout={{autosize: true}}
        useResizeHandler={true}
        style={{minHeight: "300px", height: "100%"}}
    />
}