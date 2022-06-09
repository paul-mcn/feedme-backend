const util = {
    /**
     * @param {number} min e.g. 0. Default 0
     * @param {number} max e.g. 5. Default 1
     * @returns number
     */
    getRandomNumber: (min = 0, max = 1) => {
        return Math.random() * (max - min) + min;
    },
    /**
     * @param {number} min e.g. 0. Default 0
     * @param {number} max e.g. 5. Default 10
     * @returns number
     */
    getRandomInt: (min = 0, max = 10) => {
        return Math.floor(util.getRandomNumber(min, max));
    },
    /**
     * @param {number} length the quantity of numbers in the array e.g. 2
     * @param {number} min e.g. 0. Default 0
     * @param {number} max e.g. 5. Default 10
     * @returns number
     */
    getArrayOfRandomIntegers: (length, min = 0, max = 10) => {
        let array = [];
        for (let i = 0; i < length + 1; i++) {
            const num = util.getRandomInt(min, max);
            array.push(num);
        }
        return array;
    },
    shuffleArray: (length) => {
        let array = Array.from(Array(length).keys());
        for (let i = 0; i < length; i++) {
            const randomIdx = util.getRandomInt(i, length - 1);

            const temp = array[randomIdx];
            array[randomIdx] = array[i];
            array[i] = temp;
        }
        return array
    },
    /**
     * 
     * @param {...string} args e.g. "2022-01-21T23:07:09.000Z" or same arguments for the Date Object.
     * @returns unix number
     */
    getUnixFromTimestamp(...args) {
        return Math.floor(new Date(...args).getTime() / 1000);
    }
}

module.exports = util;