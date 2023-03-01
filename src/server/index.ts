// import libraries
import express from "express";
import typeDefs from "src/schemas";
import resolvers from "src/resolvers";
import { host, port, mode } from "../config";
import database from "../db";
import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";

class Server {
  corsOrigin: string | string[];

  constructor(corsOrigin: string | string[]) {
    this.corsOrigin = corsOrigin;
  }

  private init = () => {
    database.init().then(async () => {
      // The ApolloServer constructor requires two parameters: your schema
      // definition and your set of resolvers.
      const server = new ApolloServer({
        typeDefs,
        resolvers,
      });

      // Passing an ApolloServer instance to the `startStandaloneServer` function:
      //  1. creates an Express app
      //  2. installs your ApolloServer instance as middleware
      //  3. prepares your app to handle incoming requests
      const { url } = await startStandaloneServer(server, {
        listen: { port },
      });

      if (mode !== "production") {
        const serverStartupMessage = `Server starting on ${url}/ \nGraphQL API server at ${url}/graphql 🚀🚀`;
        console.log(serverStartupMessage);
      }
    });
  };

  start = () => {
    this.init();
  };
}

export default Server;
