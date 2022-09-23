import React from "react";
import {Component as ComponentType, Dashboard, DashboardComponentTypes, Value} from "@/types";
import {gql, useQuery} from "@apollo/client";
import {Stat} from "@/components/component/text";
import {Plotly} from "@/components/component/charts";
import {Tabulator} from "@/components/component/table";
import {HTML} from "@/components/component/html";
import * as styles from "@/components/component/index.module.scss";

/*
  We'd want something a bit more complex here/with the gql for a prod system, renderType
  is the component, but the nature of the `SomeCalculateText`/deferred ones is that they
  will often override. You can set `render_type` in be also but not much thought has gone into that yet.
 */
const DashboardComponentMap = {
    [DashboardComponentTypes.Text]: HTML,
    [DashboardComponentTypes.SomeCalculateText]: HTML,
    [DashboardComponentTypes.HTML]: HTML,
    [DashboardComponentTypes.Chart]: Plotly,
    [DashboardComponentTypes.Table]: Tabulator,
    [DashboardComponentTypes.Stat]: Stat,
    [DashboardComponentTypes.Map]: Plotly,
}

type LazyComponentProps = {
    dashboard: Dashboard
    component: ComponentType
    Component: React.FC<{value: Value}>
}


const LazyComponent = ({dashboard, component, Component}: LazyComponentProps) => {
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

export const DashboardComponent = ({dashboard, component}: DashboardComponentProps) => {
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

