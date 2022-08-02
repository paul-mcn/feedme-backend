import type { Database } from '../db';
import { MealQueries } from './meals';
import type { IAddResolversToSchemaOptions } from '@graphql-tools/utils'

export const resolvers = (): any => {
    return {
        Query: {
            ...MealQueries
        },
        Mutation: {
            addMeal: async (parent: any, args: any, context: any) => {
                console.log(args)
                // const { meal } = args;
                // console.log(meal)
            }
        }
    }
}

