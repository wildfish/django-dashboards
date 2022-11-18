import {GetServerSideProps} from "next";
import client from "../../../apollo_client";
import {gql} from "@apollo/client";
import {Dashboard} from "@/types";
import {DashboardGrid, DashboardWithLayout} from "@/components/dashboard";


export const getServerSideProps: GetServerSideProps = async (context) => {
    const slug = context?.params?.slug
    const {data} = await client.query({
        query: gql`
        {
          dashboard(slug:"${slug}") {
            Meta {
              name
              slug
              layoutJson
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
    const Wrapper = dashboard.Meta.layoutJson ? DashboardWithLayout : DashboardGrid
    return <Wrapper dashboard={dashboard}/>
};

export default DashboardPage
