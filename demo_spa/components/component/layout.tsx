import React from "react";
import {
    HTMLComponent as HTMLComponentType,
    Dashboard,
    LayoutComponentTypes,
    LayoutComponent, DashboardComponentTypes,
} from "@/types";
import {HTML} from "@/components/component/html";
import * as styles from "@/components/component/index.module.scss";
import * as dashboardStyles from "@/components/dashboard/index.module.scss";
import {DashboardComponent} from "@/components/component/dashboard";


const LayoutComponentWrapperStyle = {
    [LayoutComponentTypes.Div]: styles.component,
    [LayoutComponentTypes.Card]: styles.component,
    [LayoutComponentTypes.TabContainer]: dashboardStyles.tabContainer,
    [LayoutComponentTypes.Tab]: styles.tab,
}

type HTMLComponentProps = {
    dashboard: Dashboard
    component: HTMLComponentType
}


export const HTMLComponent = ({dashboard, component}: HTMLComponentProps) => (
    <div className={dashboardStyles[`span${component.width}`]}>
        <HTML value={component.html}/>
    </div>
)


type LayoutComponentsWrapperProps = {
    dashboard: Dashboard
    layoutComponents: LayoutComponent[]
    visibleTab?: string
}


export const LayoutComponentsWrapper = ({dashboard, layoutComponents, visibleTab}: LayoutComponentsWrapperProps) => {
    return <>
        {layoutComponents.map((lc, i) => (
            (lc.renderType != LayoutComponentTypes.Tab || lc.tab_label == visibleTab) &&
            <LayoutComponentWrapper dashboard={dashboard} layoutComponent={lc} key={`wrapper${i}`}/>
        ))}
    </>
}


type ConditionalWrapperProps = {
    condition: boolean
    wrapper: (children: JSX.Element) => JSX.Element
    children: JSX.Element
}


const ConditionalWrapper = ({condition, wrapper, children}: ConditionalWrapperProps) =>
    condition ? wrapper(children) : children;


type LayoutComponentWrapperProps = {
    dashboard: Dashboard
    layoutComponent: LayoutComponent | HTMLComponentType | string | Object
}


export const LayoutComponentWrapper = ({dashboard, layoutComponent}: LayoutComponentWrapperProps) => {
    const isLayoutComponent = typeof layoutComponent === "object"
    const isTabContainer = (layoutComponent as LayoutComponent).renderType === LayoutComponentTypes.TabContainer

    let hasNested = false
    let castLayoutComponent: LayoutComponent

    if (isLayoutComponent) {
        castLayoutComponent = layoutComponent as LayoutComponent
        hasNested = isLayoutComponent && castLayoutComponent.layout_components?.length > 0
    }

    const [visibleTab, setVisibleTab] = React.useState(isTabContainer ? castLayoutComponent!.layout_components[0].tab_label : undefined)

    /*
        - Renders DashboardComponent when we are down to a string i.e the ref to put a component here.
        - else, Renders the outer LayoutComponent's class for style to be added
            - followed by nested LayoutComponentsWrapper if more nested layout_components are present
            - else, this is an HTML Component so render that.
    */
    return <>
        {isLayoutComponent && castLayoutComponent! ?
            <ConditionalWrapper
                condition={hasNested}
                wrapper={children => <div
                    className={`${LayoutComponentWrapperStyle[castLayoutComponent!.renderType]} ${dashboardStyles[`span${castLayoutComponent!.width || 6}`]}`}>{children}</div>}
            >
                <>
                    {
                        isTabContainer ?
                            <>
                                {castLayoutComponent.layout_components.map((tab, i) => {
                                    return <a className={dashboardStyles.span2}
                                              onClick={() => setVisibleTab(tab.tab_label)} key={`tab${i}`}>
                                        {tab.tab_label}
                                    </a>
                                })}
                                <LayoutComponentsWrapper dashboard={dashboard}
                                                         layoutComponents={castLayoutComponent.layout_components}
                                                         visibleTab={visibleTab}/>
                            </>
                            :
                            <>
                                {hasNested && castLayoutComponent ?
                                    <LayoutComponentsWrapper dashboard={dashboard}
                                                             layoutComponents={castLayoutComponent.layout_components}/>
                                    :
                                    <HTMLComponent dashboard={dashboard}
                                                   component={(layoutComponent as HTMLComponentType)}/>
                                }
                            </>
                    }
                </>
            </ConditionalWrapper> :
            <DashboardComponent dashboard={dashboard} component={dashboard.components.filter(c => c.key == layoutComponent)[0]}/>
        }
    </>
}
