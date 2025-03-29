import { describe, it, expect } from 'vitest';

import { extractInteger } from '$lib/extractInteger.js';

describe('extractInteger', () => {
  it('should extract the first integer from a string', () => {
    const result = extractInteger('Code-123');
    expect(result).toBe(123);
  });

  it('should handle strings with multiple integers and return the first one', () => {
    const result = extractInteger('123abc456');
    expect(result).toBe(123);
  });

  it('should return NaN if no integers are found', () => {
    const result = extractInteger('NoNumbersHere');
    expect(result).toBeNull();
  });

  it('should handle empty strings gracefully', () => {
    const result = extractInteger('');
    expect(result).toBeNull();
  });
});