import {Data} from "plotly.js";

export enum DashboardComponentTypes {
    Text = "Text",
    SomeCalculateText =  "SomeCalculateText",
    HTML =  "HTML",
    Chart =  "Chart",
    Stat =  "Stat",
    Table =  "Table",
    Map =  "Map",
}

export enum HTMLComponentTypes {
    Header = "Header",
    HTML = "HTML",
}

export enum LayoutComponentTypes {
    Div = "Div",
    Card = "Card",
}


export type Value = {
    data: Data[]
}

export type Component = {
  key: string
  value: Value | string
  width: number
  isDeferred: boolean
  renderType: DashboardComponentTypes
}

export type HTMLComponent = {
  html: string
  renderType: HTMLComponentTypes
  width?: number
}

export type DashboardMeta = {
  name: string,
  slug: string,
  layoutJson: any
}

export type Dashboard = {
  Meta: DashboardMeta
  components: Component[]
}

