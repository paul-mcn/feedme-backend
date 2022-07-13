const express = require('express');
const cors = require('cors');
const { graphqlHTTP } = require('express-graphql');
const { addResolversToSchema } = require('@graphql-tools/schema');
const schema = require('./schemas');
const { resolvers } = require('./resolvers');
const { host, port, mode } = require('./config');
const Database = require('./db');
const fs = require('fs')

const app = express();

const database = new Database()

module.exports = {
    init: async () => {
        return await database.init();
    },
    run: () => {
        const schemaResolvers = resolvers(database)

        const origin = (mode === 'development')
            ? ["http://127.0.0.1:3000", "http://localhost:3000", "http://192.168.20.14:3000"]
            : "https://organisemymeals.com"

        app.use(
            cors({
                // React server
                origin: origin,
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
    }
}
