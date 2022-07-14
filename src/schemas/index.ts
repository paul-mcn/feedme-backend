import { join } from 'path';
import { loadSchemaSync } from '@graphql-tools/load';
import { GraphQLFileLoader } from '@graphql-tools/graphql-file-loader';

const schemas = loadSchemaSync(join(__dirname, './*.graphql'), {
    loaders: [new GraphQLFileLoader()]
})

export default schemas