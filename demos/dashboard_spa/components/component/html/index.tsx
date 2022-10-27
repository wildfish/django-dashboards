import React from "react";
import {Value} from "@/types";
import * as styles from "@/components/component/index.module.scss";

export const HTML = ({value}: {value: Value}) => {
  return <div dangerouslySetInnerHTML={{ __html: value as string }}/>
}

export const CTA = ({value}: {value: Value}) => {
  return <a href={value.href} className={styles.componentCTA}>{value.text}</a>
}
