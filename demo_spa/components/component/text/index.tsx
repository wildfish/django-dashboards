import React from "react";
import {StatValue, Value} from "@/types";

export const Stat = ({value}: {value: Value}) => (
    <div>
        <h2>{(value as StatValue).text}</h2>
        <small>{(value as StatValue).sub_text}</small>
    </div>
)