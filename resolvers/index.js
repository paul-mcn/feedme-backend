
const database = require('../db/database.json')
const { shuffleArray, getUnixFromTimestamp } = require('../utils');

/**
 * @param {*[]} meals array of meals
 * @param {number} mealCount count of random meals to be returned
 * @returns meals array
 */
const filterRandomMeals = (meals, mealCount) => {
    const indexArray = shuffleArray(meals.length);
    const filteredIndexArray = indexArray.slice(0, mealCount);
    return filteredIndexArray.map(idx => meals[idx]);
}

module.exports = {
    Query: {
        meals: (parent, args, context) => {
            return database.meals
        },
        meal: (parent, args, context) => {
            const { id } = args;
            return database.meals.find(meal => meal.id === id);
        },
        mealtags: (parent, args, context) => {
            return database.mealtags
        },
        mealtag: (parent, args, context) => {
            const { id } = args;
            return database.mealtags.find(mealTag => id === mealTag.id);
        },
        suggestedMeals: (parent, args, context) => {
            // returns 7 randomly suggested meals for the week
            const { id } = args;
            const { users, meals } = database;
            // get all the suggested meals for a particular user
            const user = users.find(user => user.id === id);

            const { ids, expiryDate } = user.suggestedMeals;

            const currentDate = getUnixFromTimestamp();
            
            const hasExpired = getUnixFromTimestamp(expiryDate) < currentDate ? true : false;

            if (!ids || hasExpired) {
                const newSuggestedMeals = filterRandomMeals(meals, 7);
                // TODO: update expiry date
                // set the date 7 days from now
                // const dateOneWeekFromNow = new Date((currentDate + 60 * 60 * 24 * 7) * 1000);
                // expiryDate = dateOneWeekFromNow;
                
                return newSuggestedMeals;
            } else {
                let existingMealSuggestions = [];
                for (const meal of meals) {
                    for (const mealId of ids) {
                        if (mealId === meal.id) {
                            existingMealSuggestions.push(meal);
                        }
                    }
                }
                return existingMealSuggestions;
            }
        }
    }
}