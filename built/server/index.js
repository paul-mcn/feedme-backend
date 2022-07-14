"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const express_graphql_1 = require("express-graphql");
const schema_1 = require("@graphql-tools/schema");
const schemas_1 = __importDefault(require("../schemas"));
const resolvers_1 = require("../resolvers");
const config_1 = require("../config");
const db_1 = __importDefault(require("../db"));
const fs_1 = __importDefault(require("fs"));
const app = (0, express_1.default)();
const database = new db_1.default();
class Server {
    corsOrigin;
    constructor(corsOrigin) {
        this.corsOrigin = corsOrigin;
    }
    start() {
        database.init().then(() => {
            const schemaResolvers = (0, resolvers_1.resolvers)(database);
            app.use((0, cors_1.default)({
                // React server
                origin: this.corsOrigin,
                credentials: true
            }));
            app.use('/graphql', (0, express_graphql_1.graphqlHTTP)({
                schema: (0, schema_1.addResolversToSchema)({ schema: schemas_1.default, resolvers: schemaResolvers }),
                graphiql: (config_1.mode === 'development')
            }));
            app.use((err, req, res, next) => {
                fs_1.default.appendFile("crashlog.log", err.stack, (err) => {
                    if (err) {
                        return console.log(err);
                    }
                });
            });
            if (config_1.mode === 'development') {
                // server start-up message
                const serverStartupMessage = `Server starting on http://${config_1.host}/ \nGraphQL API server at http://${config_1.host}/graphql`;
                // port 4000
                app.listen(config_1.port, () => { console.log(serverStartupMessage); });
            }
            else {
                app.listen();
            }
        });
    }
}
exports.default = Server;
