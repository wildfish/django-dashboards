import React from "react";
import {Value} from "@/types";

export const HTML = ({value}: {value: Value}) => {
  return <div dangerouslySetInnerHTML={{ __html: value as string }}/>
}