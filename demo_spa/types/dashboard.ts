import {Data} from "plotly.js";

export enum ComponentTypes {
    Text = "Text",
    SomeCalculateText =  "SomeCalculateText",
    HTML =  "HTML",
    Chart =  "Chart",
    Stat =  "Stat",
    Table =  "Table",
    Map =  "Map",
}

export type Value = {
    data: Data[]
}

export type Component = {
  key: string
  value: Value | string
  width: number
  isDeferred: boolean
  renderType: ComponentTypes
}

export type DashboardMeta = {
  name: string,
  slug: string,
}

export type Dashboard = {
  Meta: DashboardMeta
  components: Component[]
}

