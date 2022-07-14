import type Database from '../db';
import { filterRandomMeals, getUnixFromTimestamp } from '../utils';

export const resolvers = (database: Database) => {
    return {
        Query: {
            meals: async (parent, args, context) => {
                return await database.getMeals()
            },
            meal: async (parent, args, context) => {
                const { id } = args;
                return await database.getMeal(id)
            },
            mealtags: async (parent, args, context) => {
                return await database.getMealTags()
            },
            mealtag: async (parent, args, context) => {
                const { id } = args;
                return await database.getMealTag(id)
            },
            suggestedMeals: async (parent, args, context) => {
                // returns 7 randomly suggested meals for the week
                const { id } = args;
                try {

                    const user = await database.getUser(id)
                    // get all the suggested meals for a particular user
                    if (!user) console.log(user)
                    const { ids, expiryDate } = user.suggestedMeals;

                    const currentDate = getUnixFromTimestamp();

                    const hasExpired = getUnixFromTimestamp(expiryDate) < currentDate

                    const meals = await database.getMeals()

                    if (!ids || hasExpired) {
                        const newSuggestedMeals = filterRandomMeals(meals, 7);
                        // TODO: update expiry date
                        // set the date 7 days from now
                        // const dateOneWeekFromNow = new Date((currentDate + 60 * 60 * 24 * 7) * 1000);
                        // expiryDate = dateOneWeekFromNow;

                        return newSuggestedMeals;
                    } else {
                        let existingMealSuggestions = [];
                        console.log(meals)
                        for (const meal of meals) {
                            for (const mealId of ids) {
                                if (mealId === meal.id) {
                                    existingMealSuggestions.push(meal);
                                }
                            }
                        }
                        return existingMealSuggestions;
                    }

                } catch (error) {
                    console.log(error)
                    return []
                }
            },
            favouriteMeals: async (parent, args, context) => {
                const { id } = args;

                const user = await database.getUser(id)

                const meals = await database.getMeals()

                const favouriteMeals = user.favouriteMeals.ids.map(mealId => {
                    return meals.find(meal => mealId === meal.id)
                })

                return favouriteMeals
            }
        },
        Mutation: {
            addMeal: async (parent, args, context) => {
                console.log(args)
                // const { meal } = args;
                // console.log(meal)
            }
        }
    }
}

