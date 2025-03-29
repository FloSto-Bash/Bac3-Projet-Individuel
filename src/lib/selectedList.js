import { writable } from 'svelte/store';

// Creates a writable store with an empty array, which will be shared between components
export const selectedList = writable([]);


/**
 * Update the list
 * @param {Array} arr - The new list
 */
export function updateList(arr){ 
    console.assert(arr !== undefined, 'updateList : arr is undefined');
    selectedList.set(arr);
}