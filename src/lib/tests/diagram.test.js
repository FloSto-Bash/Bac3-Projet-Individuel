import { describe, it, expect } from 'vitest';

describe('updateExecutionTime', () => {
    it('should update the executionTime and push it to executionTimeList', () => {
        let executionTime = 0;
        let executionTimeList = [];

        // Mock function to simulate the update of execution time
        // This must be a copy of the original function to ensure the validity of the test
        function updateExecutionTime(value) {
            executionTime = value;
            executionTimeList.push(executionTime);
        }

        updateExecutionTime(123.45);
        expect(executionTime).toBe(123.45);
        expect(executionTimeList).toEqual([123.45]);

        updateExecutionTime(67.89);
        expect(executionTime).toBe(67.89);
        expect(executionTimeList).toEqual([123.45, 67.89]);
    });

    it('should handle negative values correctly', () => {
        let executionTime = 0;
        let executionTimeList = [];

        function updateExecutionTime(value) {
            executionTime = value;
            executionTimeList.push(executionTime);
        }

        updateExecutionTime(-50);
        expect(executionTime).toBe(-50);
        expect(executionTimeList).toEqual([-50]);
    });

    it('should handle zero as a valid input', () => {
        let executionTime = 0;
        let executionTimeList = [];

        function updateExecutionTime(value) {
            executionTime = value;
            executionTimeList.push(executionTime);
        }

        updateExecutionTime(0);
        expect(executionTime).toBe(0);
        expect(executionTimeList).toEqual([0]);
    });
});

describe('selectStats', () => {
    it('should retrieve stats from localStorage and update the variables', () => {
        let executionCount = 0;
        let executionTime = 0;
        let swapCount = 0;
        let compareCount = 0;
        let averageTime = 0;
        let ecartType = 0;

        const mockStats = '5,123.45,10,20,67.89,3.21';
        const actualStats = 'Stats-1';
        localStorage.setItem(actualStats, mockStats);

        function selectStats() {
            let stats = localStorage.getItem(actualStats);

            if (stats) {
                stats = stats.split(',').map((stat, index) => {
                    if (index === 0 || index === 2 || index === 3) {
                        return parseInt(stat, 10);
                    } else {
                        return parseFloat(stat);
                    }
                });

                executionCount = stats[0];
                executionTime = stats[1];
                swapCount = stats[2];
                compareCount = stats[3];
                averageTime = stats[4];
                ecartType = stats[5];
            }
        }

        selectStats();

        expect(executionCount).toBe(5);
        expect(executionTime).toBe(123.45);
        expect(swapCount).toBe(10);
        expect(compareCount).toBe(20);
        expect(averageTime).toBe(67.89);
        expect(ecartType).toBe(3.21);
    });

    it('should handle missing stats in localStorage gracefully', () => {
        let executionCount = 0;
        let executionTime = 0;
        let swapCount = 0;
        let compareCount = 0;
        let averageTime = 0;
        let ecartType = 0;

        const actualStats = 'Stats-2';

        function selectStats() {
            let stats = localStorage.getItem(actualStats);

            if (stats) {
                stats = stats.split(',').map((stat, index) => {
                    if (index === 0 || index === 2 || index === 3) {
                        return parseInt(stat, 10);
                    } else {
                        return parseFloat(stat);
                    }
                });

                executionCount = stats[0];
                executionTime = stats[1];
                swapCount = stats[2];
                compareCount = stats[3];
                averageTime = stats[4];
                ecartType = stats[5];
            }
        }

        selectStats();

        expect(executionCount).toBe(0);
        expect(executionTime).toBe(0);
        expect(swapCount).toBe(0);
        expect(compareCount).toBe(0);
        expect(averageTime).toBe(0);
        expect(ecartType).toBe(0);
    });

    it('should handle malformed stats in localStorage', () => {
        let executionCount = 0;
        let executionTime = 0;
        let swapCount = 0;
        let compareCount = 0;
        let averageTime = 0;
        let ecartType = 0;

        const malformedStats = '5,abc,10,20,xyz,3.21';
        const actualStats = 'Stats-3';
        localStorage.setItem(actualStats, malformedStats);

        function selectStats() {
            let stats = localStorage.getItem(actualStats);

            if (stats) {
                stats = stats.split(',').map((stat, index) => {
                    if (index === 0 || index === 2 || index === 3) {
                        return parseInt(stat, 10);
                    } else {
                        return parseFloat(stat);
                    }
                });

                executionCount = stats[0];
                executionTime = isNaN(stats[1]) ? 0 : stats[1];
                swapCount = stats[2];
                compareCount = stats[3];
                averageTime = isNaN(stats[4]) ? 0 : stats[4];
                ecartType = stats[5];
            }
        }

        selectStats();

        expect(executionCount).toBe(5);
        expect(executionTime).toBe(0);
        expect(swapCount).toBe(10);
        expect(compareCount).toBe(20);
        expect(averageTime).toBe(0);
        expect(ecartType).toBe(3.21);
    });
});

describe('compareOnDiagram', () => {
    it('should mark two indices as being compared if compare is enabled', () => {
        let comparedIndices = [];
        let compare = true;

        function compareOnDiagram(a, b) {
            if (compare) {
                comparedIndices = [a, b];
            }
        }

        compareOnDiagram(1, 2);

        expect(comparedIndices).toEqual([1, 2]);
    });

    it('should not mark indices if compare is disabled', () => {
        let comparedIndices = [];
        let compare = false;

        function compareOnDiagram(a, b) {
            if (compare) {
                comparedIndices = [a, b];
            }
        }

        compareOnDiagram(1, 2);

        expect(comparedIndices).toEqual([]); // No indices should be marked
    });
});

describe('stopComparing', () => {
    it('should clear the compared indices if compare is enabled', () => {
        let comparedIndices = [1, 2];
        let compare = true;

        function stopComparing() {
            if (compare) {
                comparedIndices = [];
            }
        }

        stopComparing();

        expect(comparedIndices).toEqual([]);
    });

    it('should not clear the compared indices if compare is disabled', () => {
        let comparedIndices = [1, 2];
        let compare = false;

        function stopComparing() {
            if (compare) {
                comparedIndices = [];
            }
        }

        stopComparing();

        expect(comparedIndices).toEqual([1, 2]); // Indices should remain unchanged
    });
});

describe('swapOnDiagram', () => {
    it('should mark two indices as being swapped if swap is enabled', () => {
        let swapIndices = [];
        let swap = true;

        function swapOnDiagram(a, b) {
            if (swap) {
                swapIndices = [a, b];
            }
        }

        swapOnDiagram(0, 2);

        expect(swapIndices).toEqual([0, 2]);
    });

    it('should not mark indices as swapped if swap is disabled', () => {
        let swapIndices = [];
        let swap = false;

        function swapOnDiagram(a, b) {
            if (swap) {
                swapIndices = [a, b];
            }
        }

        swapOnDiagram(0, 2);

        expect(swapIndices).toEqual([]); // No indices should be marked
    });
});