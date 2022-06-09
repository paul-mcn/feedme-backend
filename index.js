const express = require('express');
const cors = require('cors');
const { graphqlHTTP } = require('express-graphql');
const { addResolversToSchema } = require('@graphql-tools/schema');
const schema = require('./schemas');
const resolvers = require('./resolvers');
const config = require('./config');

const app = express();

app.use(
    cors({
        // React server
        origin: ["http://127.0.0.1:3000", "http://localhost:3000", "http://192.168.0.212:3000"],
        credentials: true
    })
);

app.use('/graphql', graphqlHTTP({
    schema: addResolversToSchema({ schema, resolvers }),
    graphiql: true
}))

// server start-up message
const serverStartupMessage = `Server starting on http://${config.host}/ 🚀🚀\nGraphQL API server at http://${config.host}/graphql`

// port 4000
app.listen(config.port, () => console.log(serverStartupMessage));