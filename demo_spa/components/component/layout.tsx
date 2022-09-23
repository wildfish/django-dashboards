import React from "react";
import {HTMLComponent as HTMLComponentType, Dashboard, LayoutComponentTypes} from "@/types";
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


export const HTMLComponent: React.FC<HTMLComponentProps> = ({dashboard, component}) => (
    <div className={dashboardStyles[`span${component.width}`]}>
        <HTML value={component.html}/>
    </div>
)


type LayoutComponentsWrapperProps = {
    dashboard: Dashboard
    layoutComponents: []
    visibleTab?: string
}


export const LayoutComponentsWrapper: React.FC<LayoutComponentsWrapperProps> = ({dashboard, layoutComponents, visibleTab}) => {
    return <>
        {layoutComponents.map(lc => {
            return <>
                {(lc.renderType == LayoutComponentTypes.Tab && lc.tab_label != visibleTab) ?
                    <></>
                    :
                    <LayoutComponentWrapper dashboard={dashboard} layoutComponent={lc}/>
                }
            </>
        })}
    </>
}


const ConditionalWrapper = ({ condition, wrapper, children }) =>
  condition ? wrapper(children) : children;


type LayoutComponentWrapperProps = {
    dashboard: Dashboard
    layoutComponent: Object | string | HTMLComponentType
}


export const LayoutComponentWrapper: React.FC<LayoutComponentWrapperProps> = ({dashboard, layoutComponent}) => {
    const isLayoutComponent = typeof layoutComponent === "object"
    const isDashboardComponent = typeof layoutComponent === "string" || layoutComponent instanceof String
    const isTabContainer = layoutComponent.renderType === LayoutComponentTypes.TabContainer
    const hasNested = isLayoutComponent && layoutComponent?.layout_components

    const [visibleTab, setVisibleTab] = React.useState(isTabContainer ? layoutComponent?.layout_components[0].tab_label : null)

    /*
        - Renders DashboardComponent when we are down to a string i.e the ref to put a component here.
        - else, Renders the outer LayoutComponent's class for style to be added
            - followed by nested LayoutComponentsWrapper if more nested layout_components are present
            - else, this is an HTML Component so render that.
    */
    return <ConditionalWrapper
        condition={hasNested}
        wrapper={children => <div className={`${LayoutComponentWrapperStyle[layoutComponent.renderType]} ${dashboardStyles[`span${layoutComponent.width || 6}`]}`}>{children}</div>}
      >
        <>
            {
                isTabContainer ?
                    <>
                        {layoutComponent.layout_components.map(tab => {
                            return <a className={dashboardStyles.span2} onClick={() => setVisibleTab(tab.tab_label)}>
                                {tab.tab_label}
                            </a>
                        })}
                        <LayoutComponentsWrapper dashboard={dashboard} layoutComponents={layoutComponent.layout_components} visibleTab={visibleTab}/>
                    </>
                : isDashboardComponent ?
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
        </>
    </ConditionalWrapper>
}
