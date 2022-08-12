import React from "react";

export const Text: React.FC<{value: string}> = ({value}) => (
  <div>{value}</div>
)

export const HTML: React.FC<{value: string}> = ({value}) => (
  <div dangerouslySetInnerHTML={{ __html: value }}/>
)

export const Stat: React.FC<{value: {text: string, sub_text: string}}> = ({value}) => (
    <div>
        <h2>{value.text}</h2>
        <small>{value.sub_text}</small>
    </div>
)