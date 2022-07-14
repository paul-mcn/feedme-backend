"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const path_1 = require("path");
const load_1 = require("@graphql-tools/load");
const graphql_file_loader_1 = require("@graphql-tools/graphql-file-loader");
const schemas = (0, load_1.loadSchemaSync)((0, path_1.join)(__dirname, './*.graphql'), {
    loaders: [new graphql_file_loader_1.GraphQLFileLoader()]
});
exports.default = schemas;
