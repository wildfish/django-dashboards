export enum ComponentTypes {
    Text = "Text",
    SomeCalculateText =  "SomeCalculateText",
    HTML =  "HTML",
    Plotly =  "Plotly",
    Stat =  "Stat",
    Table =  "Table",
}

export type Component = {
  key: string
  value: any
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

