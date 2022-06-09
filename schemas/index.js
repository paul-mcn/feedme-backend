const { join } = require('path')
const { loadSchemaSync } = require('@graphql-tools/load');
const { GraphQLFileLoader } = require('@graphql-tools/graphql-file-loader');

const schemas = loadSchemaSync(join(__dirname, './*.graphql'), {
    loaders: [new GraphQLFileLoader()]
})

module.exports = schemas