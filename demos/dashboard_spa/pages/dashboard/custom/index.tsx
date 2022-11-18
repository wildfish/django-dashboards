import {GetServerSideProps} from "next";
import client from "../../../apollo_client";
import {gql} from "@apollo/client";
import {Dashboard} from "@/types";
import {CustomDashboard} from "@/components/dashboard";


export const getServerSideProps: GetServerSideProps = async (context) => {
    const {data} = await client.query({
        query: gql`
        {
          dashboard(slug:"dashboard-one") {
            Meta {
              name
              slug
            }
            components{
              key
              value
              gridCssClasses
              isDeferred
              renderType
            }
          }
        }
    `,
    });

    if (!data.dashboard) {
        return {notFound: true}
    }

    return {
        props: {
            dashboard: data.dashboard,
        },
    }
}


type DashboardProps = {
    dashboard: Dashboard
};


const DashboardPage = ({dashboard}: DashboardProps) => {
    return <CustomDashboard dashboard={dashboard}/>
};

export default DashboardPage
