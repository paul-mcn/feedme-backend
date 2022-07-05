const express = require('express');
const cors = require('cors');
const { graphqlHTTP } = require('express-graphql');
const { addResolversToSchema } = require('@graphql-tools/schema');
const schema = require('./schemas');
const { resolvers } = require('./resolvers');
const { host, port } = require('./config');
const Database = require('./db');

const app = express();

const database = new Database()

module.exports = {
    init: async () => {
        return await database.init();
    },
    run: () => {

        const schemaResolvers = resolvers(database)

        app.use(
            cors({
                // React server
                // origin: ["http://127.0.0.1:3000", "http://localhost:3000", "http://192.168.20.14:3000"],
                origin: "*",
                credentials: true
            })
        );

        app.use('/api/graphql', graphqlHTTP({
            schema: addResolversToSchema({ schema, resolvers: schemaResolvers }),
            graphiql: true
        }))

        // server start-up messagepauly
        const serverStartupMessage = `Server starting on http://${host}/ \nGraphQL API server at http://${host}/api/graphql`

        // port 4000
        app.listen(port, () => { console.log(serverStartupMessage) });
    }
}
