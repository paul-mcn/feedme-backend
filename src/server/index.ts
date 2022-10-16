// import libraries
import express from "express";
import cors from "cors";
import { graphqlHTTP } from "express-graphql";
import { addResolversToSchema } from "@graphql-tools/schema";
import schema from "../schemas";
import { resolvers } from "../resolvers";
import { host, port, mode } from "../config";
import database from "../db";
import fs from "fs";
import { log } from "../utils";

// import types
import type { ErrorRequestHandler, RequestHandler } from "express";

// init app
const app = express();

class Server {
  corsOrigin: string | string[];

  constructor(corsOrigin: string | string[]) {
    this.corsOrigin = corsOrigin;
  }

  private init = () => {
    database.init().then(() => {
      const schemaResolvers = resolvers();

      const errorHandler: ErrorRequestHandler = (err, req, res, next) => {
        log.createErrorLogFile("crashlog.log", err.stack);
      };

      const graphqlHttp = graphqlHTTP({
        schema: addResolversToSchema({ schema, resolvers: schemaResolvers }),
        graphiql: mode === "development",
      });

      app.use(
        cors({
          origin: this.corsOrigin,
          credentials: true,
        })
      );

      app.use("/graphql", graphqlHttp);

      app.use(errorHandler);

      if (mode === "production") {
        app.listen();
      } else {
        // server start-up message
        const serverStartupMessage = `Server starting on http://${host}/ \nGraphQL API server at http://${host}/graphql 🚀🚀`;

        // port 4000
        app.listen(port, () => {
          console.log(serverStartupMessage);
        });
      }
    });
  };

  start = () => {
    this.init();
  };
}

export default Server;
