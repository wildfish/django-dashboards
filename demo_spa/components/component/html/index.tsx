import React from "react";

export const HTML: React.FC<{value: string}> = ({value}) => (
  <div dangerouslySetInnerHTML={{ __html: value }}/>
)