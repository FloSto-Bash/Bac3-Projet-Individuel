/**
 * Pauses the execution of code for a specified number of milliseconds.
 *
 * @param {number} ms - The number of milliseconds to sleep.
 * @returns {Promise<void>} A promise that resolves after the specified duration.
 */
export function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}