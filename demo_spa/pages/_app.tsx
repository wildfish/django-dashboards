import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { ApolloProvider } from '@apollo/client';
import client from "../apollo_client";
import Link from "next/link"

function DempApp({ Component, pageProps }: AppProps) {
  return (
    <ApolloProvider client={client}>
        <small><Link href={"/"}><a>Home</a></Link> : <Link href={"/dashboard/custom"}><a>Custom</a></Link></small>

        <Component {...pageProps} />
    </ApolloProvider>
  )
}

export default DempApp
