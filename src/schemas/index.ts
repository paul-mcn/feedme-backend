import { join } from "path";
import { gql } from "apollo-server";
import {}

const schemas = loadSchemaSync(join(__dirname, "./*.graphql"), {
  loaders: [new GraphQLFileLoader()],
});

export default schemas;
