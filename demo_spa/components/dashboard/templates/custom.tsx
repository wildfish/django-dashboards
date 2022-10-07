import {DashboardComponent} from "@/components";
import React from "react";
import {Dashboard} from "@/types";


export const CustomDashboard = ({dashboard}: {dashboard: Dashboard}) => (
    <>
        <h1>Some custom title (Custom layout applied)</h1>
        <DashboardComponent dashboard={dashboard} component={dashboard.components[0]}/>
        <hr/>
        <DashboardComponent dashboard={dashboard} component={dashboard.components[1]}/>
        <hr/>
        <DashboardComponent dashboard={dashboard} component={dashboard.components[2]}/>
        <hr/>
        <DashboardComponent dashboard={dashboard} component={dashboard.components[3]}/>
    </>
)