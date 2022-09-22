import {DashboardComponent} from "@/components";
import React from "react";
import {Dashboard} from "@/types";


export const DashboardGrid: React.FC<{dashboard: Dashboard}> = ({dashboard}) => (
    <>
        <h1>{dashboard.Meta.name} (Grid applied)</h1>
        <div className="dashboard-container">
        {dashboard.components.map(c =>
            <div className={`dashboard-component span-${c.width || 4}`} key={c.key} >
                <DashboardComponent dashboard={dashboard} component={c}/>
            </div>
        )}
        </div>
    </>
)