import type { Database } from "../db";
import { MealQueries } from "./meals";

const resolvers = {
  Query: {
    ...MealQueries,
  },
  Mutation: {
    addMeal: async (parent: any, args: any, context: any) => {
      console.log(args);
      // const { meal } = args;
      // console.log(meal)
    },
  },
};

export default resolvers;
