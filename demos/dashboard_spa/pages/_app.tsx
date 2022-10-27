import '../styles/globals.scss'
import type { AppProps } from 'next/app'
import { ApolloProvider } from '@apollo/client';
import client from "../apollo_client";
import Link from "next/link"
import { FilterProvider } from "../appContext";

function DempApp({ Component, pageProps }: AppProps) {
  return (
    <ApolloProvider client={client}>
        <FilterProvider>
            <div className="content">
                <small>
                    <Link href={"/"}><a>Grid</a></Link> |&nbsp;
                    <Link href={"/dashboard/dashboard-one-vary"}><a>With Layout</a></Link> |&nbsp;
                    <Link href={"/dashboard/custom"}><a>Custom</a></Link>
                </small>

                <Component {...pageProps} />
            </div>
        </FilterProvider>
    </ApolloProvider>
  )
}

export default DempApp
