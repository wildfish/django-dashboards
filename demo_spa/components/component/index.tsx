import React from "react";
import {Component as ComponentType, HTMLComponent as HTMLComponentType, Dashboard, DashboardComponentTypes, LayoutComponentTypes} from "@/types";
import {gql, useQuery} from "@apollo/client";
import {Stat, Text} from "@/components/component/text";
import {Plotly} from "@/components/component/charts";
import {Tabulator} from "@/components/component/table";
import {HTML} from "@/components/component/html";
import * as styles from "@/components/component/index.module.scss";
import * as dashboardStyles from "@/components/dashboard/index.module.scss";

/*
  We'd want something a bit more complex here/with the gql for a prod system, renderType
  is the component, but the nature of the `SomeCalculateText`/deferred ones is that they
  will often override. You can set `render_type` in be also but not much thought has gone into that yet.
 */
const DashboardComponentMap = {
    [DashboardComponentTypes.Text]: Text,
    [DashboardComponentTypes.SomeCalculateText]: Text,
    [DashboardComponentTypes.HTML]: HTML,
    [DashboardComponentTypes.Chart]: Plotly,
    [DashboardComponentTypes.Table]: Tabulator,
    [DashboardComponentTypes.Stat]: Stat,
    [DashboardComponentTypes.Map]: Plotly,
}

type LazyComponentProps = {
    dashboard: Dashboard
    component: ComponentType
    Component: React.FC<{value: string}>
}


const LazyComponent: React.FC<LazyComponentProps> = ({dashboard, component, Component}) => {
    const { loading, data } = useQuery(gql`
      {
        component(slug:"${dashboard.Meta.slug}", key: "${component.key}") {
          value
        }
      }
    `);

    return <>
       {loading || !data ? <>Loading...</> : <Component value={data.component.value}/>}
    </>
};

type DashboardComponentProps = {
    dashboard: Dashboard
    component: ComponentType
    className?: string
}

export const DashboardComponent: React.FC<DashboardComponentProps> = ({dashboard, component}) => {
    const Component = DashboardComponentMap[component.renderType]
    return <div className={styles.componentInner}>
        {Object.keys(DashboardComponentMap).includes(component.renderType) ?
            !component.isDeferred ?
                <Component value={component.value}/>
            :
                <LazyComponent dashboard={dashboard} component={component} Component={Component}/>
        :
            <div>Missing dashboard component mapping</div>
        }
    </div>
}


type HTMLComponentProps = {
    dashboard: Dashboard
    component: HTMLComponentType
}

export const HTMLComponent: React.FC<HTMLComponentProps> = ({dashboard, component}) => (
    <div className={dashboardStyles[`span${component.width}`]}>
        <HTML value={component.html}/>
    </div>
)

type LayoutComponentsWrapperProps = {
    dashboard: Dashboard
    layoutComponents: []
}


export const LayoutComponentsWrapper: React.FC<LayoutComponentsWrapperProps> = ({dashboard, layoutComponents}) => {
    return <>
        {layoutComponents.map(lc => (
            <LayoutComponentWrapper dashboard={dashboard} layoutComponent={lc}/>
        ))}
    </>
}


type LayoutComponentWrapperProps = {
    dashboard: Dashboard
    layoutComponent: Object | string | HTMLComponentType
}


const LayoutComponentWrapperStyle = {
    [LayoutComponentTypes.Div]: styles.component,
    [LayoutComponentTypes.Card]: styles.component,
}

const ConditionalLayoutComponentWrapper = ({ condition, wrapper, children }) =>
  condition ? wrapper(children) : children;



export const LayoutComponentWrapper: React.FC<LayoutComponentWrapperProps> = ({dashboard, layoutComponent}) => {
    const isLayoutComponent = typeof layoutComponent === "object"
    const isDashboardComponent = typeof layoutComponent === "string" || layoutComponent instanceof String
    const hasNested = isLayoutComponent && layoutComponent?.layout_components

    /*
        - Renders DashboardComponent when we are down to a string i.e the ref to put a component here.
        - else, Renders the outer LayoutComponent's class for style to be added
            - followed by nested LayoutComponentsWrapper if more nested layout_components are present
            - else, this is an HTML Component so render that.
    */

    return <ConditionalLayoutComponentWrapper
        condition={hasNested}
        wrapper={children => <div className={`${LayoutComponentWrapperStyle[layoutComponent.renderType]} ${dashboardStyles[`span${layoutComponent.width || 6}`]}`}>{children}</div>}
      >
        {isDashboardComponent ?
            <DashboardComponent dashboard={dashboard} component={dashboard.components.find(c => c.key == layoutComponent)}/>
            :
            <>
                {
                    hasNested ?
                        <LayoutComponentsWrapper dashboard={dashboard} layoutComponents={layoutComponent.layout_components}/>
                        :
                        <HTMLComponent dashboard={dashboard} component={layoutComponent}/>
                }
            </>
        }
    </ConditionalLayoutComponentWrapper>
}
