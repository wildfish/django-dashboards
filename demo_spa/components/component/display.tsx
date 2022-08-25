import React from "react";
import {Component, Dashboard, ComponentTypes} from "@/types";
import {gql, useQuery} from "@apollo/client";
import {HTML, Stat, Text} from "@/components/component/text";
import {Plotly} from "@/components/component/charts";
import {Tabulator} from "@/components/component/table";

/*
  We'd want something a bit more complex here/with the gql for a prod system, renderType
  is the component, but the nature of the `SomeCalculateText`/deferred ones is that they
  will often override. You can set `render_type` in be also but not much thought has gone into that yet.
 */
const ComponentToDisplay = {
    [ComponentTypes.Text]: Text,
    [ComponentTypes.SomeCalculateText]: Text,
    [ComponentTypes.HTML]: HTML,
    [ComponentTypes.Chart]: Plotly,
    [ComponentTypes.Table]: Tabulator,
    [ComponentTypes.Stat]: Stat,
}

type LazyComponentProps = {
    dashboard: Dashboard
    component: Component
    Display: React.FC<{value: string}>
}


const LazyComponent: React.FC<LazyComponentProps> = ({dashboard, component, Display}) => {
    const { loading, data } = useQuery(gql`
      {
        component(slug:"${dashboard.Meta.slug}", key: "${component.key}") {
          value
        }
      }
    `);

    return <>
       {loading ? <>Loading...</> : <Display value={data?.component.value}/>}
    </>
};

type DisplayComponentProps = {
    dashboard: Dashboard
    component: Component
    className?: string
}

export const DisplayComponent: React.FC<DisplayComponentProps> = ({dashboard, component}) => {
    const Display = ComponentToDisplay[component.renderType]
    return <>
        {Object.keys(ComponentTypes).includes(component.renderType) ?
            !component.isDeferred ?
                <Display value={component.value}/>
            :
                <LazyComponent dashboard={dashboard} component={component} Display={Display}/>
        :
            <div>Missing component mapping</div>
        }
    </>
}
