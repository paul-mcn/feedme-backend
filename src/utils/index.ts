import type { Meal } from "../db/interfaces";

/**
 * @param {number} min e.g. 0. Default 0
 * @param {number} max e.g. 5. Default 1
 * @returns number
 */
export const getRandomNumber = (min: number = 0, max: number = 1) => {
    return Math.random() * (max - min) + min;
}

/**
 * @param {number} min e.g. 0. Default 0
 * @param {number} max e.g. 5. Default 10
 * @returns number
 */
export const getRandomInt = (min: number = 0, max: number = 10) => {
    return Math.floor(getRandomNumber(min, max));
}

/**
 * @param {number} length the quantity of numbers in the array e.g. 2
 * @param {number} min e.g. 0. Default 0
 * @param {number} max e.g. 5. Default 10
 * @returns number
 */
export const getArrayOfRandomIntegers = (length: number, min: number = 0, max: number = 10) => {
    let array: number[] = [];
    for (let i = 0; i < length + 1; i++) {
        const num = getRandomInt(min, max);
        array.push(num);
    }
    return array;
}

export const shuffleArray = (length) => {
    let array = Array.from(Array(length).keys());
    for (let i = 0; i < length; i++) {
        const randomIdx = getRandomInt(i, length - 1);

        const temp = array[randomIdx];
        array[randomIdx] = array[i];
        array[i] = temp;
    }
    return array
}

/**
 * Gets time in UNIX from timestamp. If no args supplied then time will be created from now.
 * @param {string | number | Date} args e.g. "2022-01-21T23:07:09.000Z" or same arguments for the Date Object.
 * @returns unix number
 */
export const getUnixFromTimestamp = (args?: string | number | Date) => {
    return Math.floor(new Date(args).getTime() / 1000);
}

/**
 * @param {Meal[]} meals array of meals
 * @param {number} mealCount count of random meals to be returned
 * @returns meals array
 */
export const filterRandomMeals = (meals: Meal[], mealCount: number) => {
    const indexArray = shuffleArray(meals.length);
    const filteredIndexArray = indexArray.slice(0, mealCount);
    return filteredIndexArray.map(idx => meals[idx]);
}