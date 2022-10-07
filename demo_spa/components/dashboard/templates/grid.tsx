import {DashboardComponent} from "@/components";
import React from "react";
import {Dashboard} from "@/types";
import * as styles from "@/components/dashboard/index.module.scss";
import * as componentStyles from "@/components/component/index.module.scss";


export const DashboardGrid = ({dashboard}: {dashboard: Dashboard}) => (
    <>
        <h1>{dashboard.Meta.name} (Grid applied)</h1>
        <div className={styles.dashboardContainer}>
        {dashboard.components.map(c =>
            <div className={`${componentStyles.component} ${styles[`span${c.width}`]}`} key={c.key}>
                <DashboardComponent dashboard={dashboard} component={c}/>
            </div>
        )}
        </div>
    </>
)