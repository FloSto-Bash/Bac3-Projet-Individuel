<script>
    import { onMount } from 'svelte';
    import { scaleLinear } from 'd3-scale';
    import { fly } from 'svelte/transition';

    import { selectedList } from '../../lib/selectedList.js';
    import { get, writable } from 'svelte/store';

    // Get the unsorted lists from the parent component
    let { unsortedLists, isDarkMode, pyscriptReady, actualCode, extractInteger } = $props();

    // init variables for localStorage
    let keys = writable([]);
    let actualStats = $derived('Stats-' + String(extractInteger(actualCode)));

    // Define the state variables
    let comparedIndices = $state([]);
    let swapIndices = $state([]);

    let compare = $state(true);
    let swap = $state(true);

    let selectedListName = $state(unsortedLists[0].name);

    let width = $state(undefined);
    let height = $state(undefined);

    let executionCount = $state(0);

    let inExecution = $state(false);

    // Define the stats variables
    let executionTime = $state(0);
    let executionTimeList = $state([]);
    let swapCount = $state(0);
    let compareCount = $state(0);
    let averageTime = $state(0);
    let ecartType = $state(0);
    let allStats = $derived([executionCount, executionTime.toFixed(3), swapCount, compareCount, averageTime.toFixed(3), ecartType.toFixed(3)]);

    const maxAnimation = 50;
    let animationInput = $state(maxAnimation/2);
    let animationTime = $derived(computeAnimationTime(animationInput));

    const arrayLength = $derived(get(selectedList).length);

    const padding = { top: 20, right: 20, bottom: 20, left: 20 };

    /**
     * Compute the animation time based on the input
     * Note : The animation time is computed as 50 * (maxAnimation - animationInput), 50 an arbitrary value in milliseconds
     */
    function computeAnimationTime() {
        return 50 * (maxAnimation - animationInput);
    }

    function syncStatsWithLocalStorage() {
        if (localStorage.getItem(actualStats) !== null ) return;

        resetStats();
        const interval = setInterval( async () => {
            localStorage.setItem(actualStats, allStats);
            keys.set(Object.keys(localStorage));
        }, 2000);

        return () => clearInterval(interval);
    };

    /**
     * On mount, reset the grid to the selected list and set the window functions and variables
    */
    onMount(() => {

        resetGrid();

        window.compareOnDiagram = compareOnDiagram;
        window.stopComparing = stopComparing;

        window.swapOnDiagram = swapOnDiagram;

        window.getCompare = () => compare;
        window.getSwap = () => swap;

        window.resetGrid = resetGrid;

        window.incrementExecutionCount = () => executionCount = executionCount + 1;
        window.decrementExecutionCount = () => { if (executionCount > 0) { executionCount = executionCount - 1; } };
        window.updateInExecution = (value) => inExecution = value;
        window.updateExecutionTime = updateExecutionTime;
        window.updateSwapCount = (value) => swapCount = value;
        window.updateCompareCount = (value) => compareCount = value;
        window.updateAverageTime = (value) => averageTime = value;
        window.updateStandardDeviation = (value) => ecartType = value;

        window.getExecutionCount = () => executionCount;
        window.getExecutionTime = () => executionTime;
        window.getAverageTime = () => averageTime;
        window.getEcartType = () => ecartType;
        window.getExecutionTimeList = () => executionTimeList;

        window.getAnimationTime = () => animationTime;
        window.addStats = () => syncStatsWithLocalStorage();;
        window.deleteStats = (key) => deleteLocalStorageStats(key);
        window.selectLocalStorageStats = () => selectStats();

        if (localStorage.getItem(actualStats) === null) {
            keys.set(Object.keys(localStorage));
            syncStatsWithLocalStorage();
        } else {
            selectStats();
        }
    });

    $effect(() => {
        localStorage.setItem(actualStats, allStats);
        keys.set(Object.keys(localStorage));
    })

    function deleteLocalStorageStats(key) {
        key = "Stats-" + String(extractInteger(key));
        localStorage.removeItem(key);
        keys.set(Object.keys(localStorage));
    }

    function updateExecutionTime (value) {
        executionTime = value;
        executionTimeList.push(executionTime);
    }

    function selectStats() {
        // executionCount, executionTime, swapCount, compareCount, averageTime, ecartType = localStorage.getItem(actualStats);
        let stats = localStorage.getItem(actualStats);
        
        // Code from GitHub Copilot
        if (stats) {
        stats = stats.split(',').map((stat, index) => {
            if (index === 0 || index === 2 || index === 3) {
                return parseInt(stat, 10);
            } else {
                return parseFloat(stat);
            }
        });

        // Assigner les valeurs aux variables correspondantes
        executionCount = stats[0];
        executionTime = stats[1];
        swapCount = stats[2];
        compareCount = stats[3];
        averageTime = stats[4];
        ecartType = stats[5];
    }
    }

    const xScale = $derived(scaleLinear().domain([0, arrayLength]).range([padding.left, width - padding.right]));

    const yScale = $derived(scaleLinear().domain([0, Math.max(...get(selectedList))]).range([height - padding.bottom, padding.top]));
        
    const innerWidth = $derived(width - (padding.left + padding.right));
    const barWidth = $derived(innerWidth / arrayLength);

    /**
     * Reset the grid to the selected list
    */
    function resetGrid() {
        let foundList = unsortedLists.find(list => list.name === selectedListName);
        console.assert(foundList !== undefined || foundList !== null, 'foundList is undefined or null');
        console.assert(Array.isArray(foundList.value), 'foundList.value is not an array');
        if (foundList) {
            selectedList.set([...foundList.value]);
        }
        swapCount = 0;
        compareCount = 0;
    }

    /**
     * Compare two elements on the diagram
     * @param {number} a
     * @param {number} b
    */
    async function compareOnDiagram(a, b) {
        if (compare) {comparedIndices = [a, b];}
    }

    /**
     * Stop comparing elements on the diagram
    */
    async function stopComparing() {
        if (compare) {comparedIndices = [];}
    }

    /**
     * Swap two elements on the diagram
     * @param {number} a
     * @param {number} b
    */
    async function swapOnDiagram(a, b) {
        if (swap) {swapIndices = [a, b];}
    }

    function resetStats() {
        executionTimeList = [];

        executionTime = 0;
        swapCount = 0;
        compareCount = 0;
        averageTime = 0;
        ecartType = 0;
        executionCount = 0;
    }

    /**
     * Set a timeout to reset the swap indices, after a certain time
     * @param {number} time
    */
    $effect(() => {
        if (swapIndices.length > 0) {
            setTimeout(() => (swapIndices = []), animationTime);
        };
    });
</script>

<svelte:head>
    <script type="module" src="https://pyscript.net/releases/2025.2.3/core.js"></script>
    <script type="py" src="python/main.py" config="python/config/pyscript.json"></script>
</svelte:head>

<div class="form-control flex flex-col items-center">
    <select bind:value={selectedListName} onchange={resetGrid} class="select select-primary select-xs sm:select-sm w-full max-w-xs mb-4" style="text-align-last:center;" disabled={inExecution}>
        {#each unsortedLists as list}
            <option value={list.name}>{list.name}</option>
        {/each}
    </select>

    <label class="label cursor-pointer">
        <input type="checkbox" class="checkbox checkbox-primary checkbox-sm" bind:checked={compare} onclick={() => { stopComparing(); compare = !compare; }}/>
        <span class="label-text ml-2"> Show compare</span>
    </label>

    <label class="label cursor-pointer">
        <input type="checkbox" class="checkbox checkbox-primary checkbox-sm" bind:checked={swap} onclick={() => swap = !swap}/>
        <span class="label-text ml-2">Show swap</span>
    </label>
</div>

<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
    <svg style="width: 100%; height: 100%;">
        <g class="bars">
            {#each $selectedList as value, i}
                <!-- Make a transition if the elements need to be swapped -->
                {#if swapIndices.includes(i)}
                    <rect
                        transition:fly={{ x: xScale(swapIndices[1 - swapIndices.indexOf(i)]) - xScale(i), duration: animationTime}}
                        x={xScale(i) + 2 || 0}
                        y={yScale(value) || 0}
                        width={(width < 512 ? barWidth - 2 : barWidth - 4)|| 0}
                        height={Math.abs(yScale(0) - yScale(value)) || 0}
                        fill={comparedIndices.includes(i) ? '#FF9900' : '#B40000'}
                    />
                {:else}
                    <rect
                        x={xScale(i) + 2 || 0}
                        y={yScale(value) || 0}
                        width={(width < 512 ? barWidth - 2 : barWidth - 4)|| 0}
                        height={Math.abs(yScale(0) - yScale(value)) || 0}
                        fill={comparedIndices.includes(i) ? '#FF9900' : '#B40000'}
                    />
                {/if}
            {/each}
        </g>
    </svg>
</div>

<div class="join join-horizontal flex justify-center mt-4 mb">
    <button class="join-item btn btn-xs sm:btn-sm md:btn-md" onclick={resetGrid} aria-label="Unsort the grid" disabled={inExecution}>
        <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 512 512" fill={isDarkMode ? 'white' : 'black'}>
            <path d="M403.8 34.4c12-5 25.7-2.2 34.9 6.9l64 64c6 6 9.4 14.1 9.4 22.6s-3.4 16.6-9.4 22.6l-64 64c-9.2 9.2-22.9 11.9-34.9 6.9s-19.8-16.6-19.8-29.6l0-32-32 0c-10.1 0-19.6 4.7-25.6 12.8L284 229.3 244 176l31.2-41.6C293.3 110.2 321.8 96 352 96l32 0 0-32c0-12.9 7.8-24.6 19.8-29.6zM164 282.7L204 336l-31.2 41.6C154.7 401.8 126.2 416 96 416l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32l64 0c10.1 0 19.6-4.7 25.6-12.8L164 282.7zm274.6 188c-9.2 9.2-22.9 11.9-34.9 6.9s-19.8-16.6-19.8-29.6l0-32-32 0c-30.2 0-58.7-14.2-76.8-38.4L121.6 172.8c-6-8.1-15.5-12.8-25.6-12.8l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32l64 0c30.2 0 58.7 14.2 76.8 38.4L326.4 339.2c6 8.1 15.5 12.8 25.6 12.8l32 0 0-32c0-12.9 7.8-24.6 19.8-29.6s25.7-2.2 34.9 6.9l64 64c6 6 9.4 14.1 9.4 22.6s-3.4 16.6-9.4 22.6l-64 64z"/>
        </svg>
    </button>
    {#if !pyscriptReady}
    <button class="join-item btn btn-xs sm:btn-sm md:btn-md" aria-label="Loading">
        <span class="loading loading-spinner loading-xs sm:loading-sm md:loading-md "></span>
    </button>
    {:else}
    <button class="join-item btn btn-xs sm:btn-sm md:btn-md" onclick={resetGrid} py-click='startWorker' id='buttonExec' disabled={inExecution} aria-label="Execute the algorithm">
        <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 384 512" fill={isDarkMode ? 'white' : 'black'}>
            <path d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80L0 432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"/>
        </svg>
    </button>
    {/if}
    <button class="join-item btn btn-xs sm:btn-sm md:btn-md" onclick={resetStats} aria-label="Reset Stats" disabled={inExecution}>
        <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 512 512" fill={isDarkMode ? 'white' : 'black'}>
            <path d="M463.5 224l8.5 0c13.3 0 24-10.7 24-24l0-128c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1c-87.5 87.5-87.5 229.3 0 316.8s229.3 87.5 316.8 0c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0c-62.5 62.5-163.8 62.5-226.3 0s-62.5-163.8 0-226.3c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8l119.5 0z"/>
        </svg>
    </button>
</div>

<div>
    <label class="flex justify-center text-xs md:text-md lg:text-lg m-2" for="animationInput">Customize the Animation</label>
    <input id="animationInput" type="range" min="1" max={maxAnimation - 1} bind:value={animationInput} class="flex justify-center range range-primary w-1/2 md:w-1/2 lg:w-1/3 xl:w-1/3 mx-auto mb-1"/>
        <div class="flex justify-between px-2 text-xs md:text-md w-1/2 md:w-1/2 lg:w-1/3 xl:w-1/3 mx-auto mb-2">
            <span>slow</span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span>fast</span>
        </div>
</div>

<div class="overflow-x-auto">
    <table class="table table-xs sm:table-sm md:table-md lg:table-lg xl:table-xl">
        <thead class="bg-base-200">
            <tr>
            <th>Execution Count</th>
            <th>Execution Time</th>
            <th>Swap Count</th>
            <th>Compare Count</th>
            <th>Average Time</th>
            <th>Standard Deviation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td>{allStats[0]}</td>
            <td>{allStats[1]}</td>
            <td>{allStats[2]}</td>
            <td>{allStats[3]}</td>
            <td>{allStats[4]}</td>
            <td>{allStats[5]}</td>
            </tr>
        </tbody>
    </table>
</div>