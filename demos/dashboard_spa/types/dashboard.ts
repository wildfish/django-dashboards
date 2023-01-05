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
    CTA = "CTA",
}

export enum HTMLComponentTypes {
    Header = "Header",
    HTML = "HTML",
    HR = "HR",
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

export type CTAValue = {
    text: string, href: string
}


export type Value = DataValue | StatValue | CTAValue | string


export type Component = {
  key: string
  value: Value
  gridCssClasses: string
  isDeferred: boolean
  renderType: DashboardComponentTypes
}


export type LayoutComponent = {
  layout_components: LayoutComponent[],
  renderType: LayoutComponentTypes
  gridCssClasses: string
  tab_label?: string
}


export type HTMLComponent = {
  html: string
  renderType: HTMLComponentTypes
}


export type DashboardMeta = {
  name: string,
  verbose_name: string,
  slug: string,
  layoutJson: any
}


export type Dashboard = {
  Meta: DashboardMeta
  components: Component[]
}

