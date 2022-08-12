import {DisplayComponent} from "@/components";
import React from "react";
import {Dashboard} from "@/types";


export const CustomDashboard: React.FC<{dashboard: Dashboard}> = ({dashboard}) => (
    <>
        <h1>Some custom title</h1>
        <DisplayComponent dashboard={dashboard} component={dashboard.components[0]}/>
        <hr/>
        <DisplayComponent dashboard={dashboard} component={dashboard.components[1]}/>
        <hr/>
        <DisplayComponent dashboard={dashboard} component={dashboard.components[2]}/>
        <hr/>
        <DisplayComponent dashboard={dashboard} component={dashboard.components[3]}/>
    </>
)