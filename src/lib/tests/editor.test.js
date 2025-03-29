import { describe, it, expect, vi } from 'vitest';

import { selectedList, updateList } from '$lib/selectedList.js';

describe('updateList', () => {
    it('should update the selectedList with the provided array', async () => {
        const newList = [1, 2, 3];
        updateList(newList);
  
        selectedList.subscribe((value) => {
            expect(value).toEqual(newList);
        })();
    });
  
    it('should throw a console error if the array is undefined', async () => {
        const consoleSpy = vi.spyOn(console, 'assert');
        updateList(undefined);
    
        expect(consoleSpy).toHaveBeenCalledWith(false, 'updateList : arr is undefined');
        consoleSpy.mockRestore();
    });
  });