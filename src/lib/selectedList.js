import { writable } from 'svelte/store';

// Creates a writable store with an empty array, which will be shared between components
export const selectedList = writable([]);