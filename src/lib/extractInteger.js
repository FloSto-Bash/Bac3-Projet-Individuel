/**
 * Extract the integer from a string
 * @param {string} str - The string to extract the integer from
 * @returns {Number|null} - The extracted integer or null if not found
 * @example - extractInteger("Code-1") => 1
 * @example - extractInteger("Code-abc") => null
 */
export function extractInteger(str) {
    const matches = str.match(/\d+/g);
    return matches ? matches.map(Number)[0] : null;
}