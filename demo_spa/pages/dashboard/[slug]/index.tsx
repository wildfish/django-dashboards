import {GetServerSideProps} from "next";
import client from "../../../apollo_client";
import {gql} from "@apollo/client";
import {Dashboard} from "@/types";
import {DashboardGrid} from "@/components/dashboard";
import {DashboardWithLayout} from "@/components/dashboard/layout";


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
              width
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


const DashboardPage: React.FC<DashboardProps> = ({dashboard}) => {
    const Wrapper = dashboard.Meta.layoutJson ? DashboardWithLayout : DashboardGrid
    return <Wrapper dashboard={dashboard}/>
};

export default DashboardPage
