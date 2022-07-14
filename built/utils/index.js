"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.filterRandomMeals = exports.getUnixFromTimestamp = exports.shuffleArray = exports.getArrayOfRandomIntegers = exports.getRandomInt = exports.getRandomNumber = void 0;
/**
 * @param {number} min e.g. 0. Default 0
 * @param {number} max e.g. 5. Default 1
 * @returns number
 */
const getRandomNumber = (min = 0, max = 1) => {
    return Math.random() * (max - min) + min;
};
exports.getRandomNumber = getRandomNumber;
/**
 * @param {number} min e.g. 0. Default 0
 * @param {number} max e.g. 5. Default 10
 * @returns number
 */
const getRandomInt = (min = 0, max = 10) => {
    return Math.floor((0, exports.getRandomNumber)(min, max));
};
exports.getRandomInt = getRandomInt;
/**
 * @param {number} length the quantity of numbers in the array e.g. 2
 * @param {number} min e.g. 0. Default 0
 * @param {number} max e.g. 5. Default 10
 * @returns number
 */
const getArrayOfRandomIntegers = (length, min = 0, max = 10) => {
    let array = [];
    for (let i = 0; i < length + 1; i++) {
        const num = (0, exports.getRandomInt)(min, max);
        array.push(num);
    }
    return array;
};
exports.getArrayOfRandomIntegers = getArrayOfRandomIntegers;
const shuffleArray = (length) => {
    let array = Array.from(Array(length).keys());
    for (let i = 0; i < length; i++) {
        const randomIdx = (0, exports.getRandomInt)(i, length - 1);
        const temp = array[randomIdx];
        array[randomIdx] = array[i];
        array[i] = temp;
    }
    return array;
};
exports.shuffleArray = shuffleArray;
/**
 * Gets time in UNIX from timestamp. If no args supplied then time will be created from now.
 * @param {string | number | Date} args e.g. "2022-01-21T23:07:09.000Z" or same arguments for the Date Object.
 * @returns unix number
 */
const getUnixFromTimestamp = (args) => {
    return Math.floor(new Date(args).getTime() / 1000);
};
exports.getUnixFromTimestamp = getUnixFromTimestamp;
/**
 * @param {Meal[]} meals array of meals
 * @param {number} mealCount count of random meals to be returned
 * @returns meals array
 */
const filterRandomMeals = (meals, mealCount) => {
    const indexArray = (0, exports.shuffleArray)(meals.length);
    const filteredIndexArray = indexArray.slice(0, mealCount);
    return filteredIndexArray.map(idx => meals[idx]);
};
exports.filterRandomMeals = filterRandomMeals;
