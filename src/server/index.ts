import express from 'express'
import cors from 'cors'
import { graphqlHTTP } from 'express-graphql';
import { addResolversToSchema } from '@graphql-tools/schema';
import schema from '../schemas';
import { resolvers } from '../resolvers';
import { host, port, mode } from '../config';
import Database from '../db';
import fs from 'fs';

const app = express();

const database = new Database()

class Server {
    corsOrigin: string | string[]
    
    constructor(corsOrigin: string | string[]) {
        this.corsOrigin = corsOrigin
    }

    start() {
        database.init().then(() => {
            const schemaResolvers = resolvers(database)

            app.use(
                cors({
                    // React server
                    origin: this.corsOrigin,
                    credentials: true
                })
            );

            app.use('/graphql', graphqlHTTP({
                schema: addResolversToSchema({ schema, resolvers: schemaResolvers }),
                graphiql: (mode === 'development')
            }))

            app.use((err, req, res, next) => {
                fs.appendFile("crashlog.log", err.stack, (err) => {
                    if (err) {
                        return console.log(err)
                    }
                })
            })

            if (mode === 'development') {
                // server start-up message
                const serverStartupMessage = `Server starting on http://${host}/ \nGraphQL API server at http://${host}/graphql`
                // port 4000
                app.listen(port, () => { console.log(serverStartupMessage) });
            } else {
                app.listen();
            }
        });
    }
}

export default Server
