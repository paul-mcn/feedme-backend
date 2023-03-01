import { random } from "../utils";
import getUnixTime from "date-fns/getUnixTime";
import database from "../db";

// TODO move queries to their respective folders

export const MealQueries = {
  meals: async (parent: any, args: any, context: any) => {
    return await database.getMeals();
  },
  meal: async (parent: any, args: any, context: any) => {
    const { id } = args;
    return await database.getMeal(id);
  },
  mealtags: async (parent: any, args: any, context: any) => {
    return await database.getMealTags();
  },
  mealtag: async (parent: any, args: any, context: any) => {
    const { id } = args;
    return await database.getMealTag(id);
  },
  suggestedMeals: async (parent: any, args: any, context: any) => {
    // returns 7 randomly suggested meals for the week
    const { id } = args;
    try {
      const user = await database.getUser(id);
      // get all the suggested meals for a particular user
      if (!user) console.log(user);
      const { ids: favMealIds, expiryDate } = user.suggestedMeals;

      const currentDate = getUnixTime(new Date());

      const hasExpired = getUnixTime(expiryDate) < currentDate;

      const meals = await database.getMeals();

      if (favMealIds && !hasExpired) {
        const CACHE = {};
        meals.forEach((meal, idx) => (CACHE[meal.id] = idx));
        const favMeals = favMealIds.map((favMealId) => meals[CACHE[favMealId]]);
        return favMeals;
      } else {
        const newSuggestedMeals = random.filterRandomMeals(meals, 7);
        // TODO: update expiry date
        // set the date 7 days from now
        // const dateOneWeekFromNow = new Date((currentDate + 60 * 60 * 24 * 7) * 1000);
        // expiryDate = dateOneWeekFromNow;

        return newSuggestedMeals;
      }
    } catch (error) {
      console.log(error);
      return [];
    }
  },
  favouriteMeals: async (parent: any, args: any, context: any) => {
    const { id } = args;

    const user = await database.getUser(id);

    const meals = await database.getMeals();

    const favouriteMeals = user.favouriteMeals.ids.map((mealId) => {
      return meals.find((meal) => mealId === meal.id);
    });

    return favouriteMeals;
  },
};
