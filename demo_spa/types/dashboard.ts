import {Data} from "plotly.js";

export enum DashboardComponentTypes {
    Text = "Text",
    SomeCalculateText =  "SomeCalculateText",
    HTML =  "HTML",
    Chart =  "Chart",
    Stat =  "Stat",
    Table =  "Table",
    Map =  "Map",
    Form =  "Form",
}

export enum HTMLComponentTypes {
    Header = "Header",
    HTML = "HTML",
}

export enum LayoutComponentTypes {
    Div = "Div",
    Card = "Card",
    TabContainer = "TabContainer",
    Tab = "Tab",
}


export type DataValue = {
    data: Data[]
}


export type StatValue = {
    text: string, sub_text: string
}


export type Value = DataValue | StatValue | string


export type Component = {
  key: string
  value: Value
  width: number
  isDeferred: boolean
  renderType: DashboardComponentTypes
}


export type LayoutComponent = {
  layout_components: LayoutComponent[],
  renderType: LayoutComponentTypes
  width: number
  tab_label?: string
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

