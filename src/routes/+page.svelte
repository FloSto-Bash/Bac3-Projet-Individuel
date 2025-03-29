<!-- All svg files are coming from : Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc. -->
<script>
  import Editor from "./components/editor.svelte";
  import Diagram from "./components/diagram.svelte";

  import { get } from "svelte/store";

  import { selectedList } from "../lib/selectedList.js";
  import { unsortedLists } from "../lib/unsortedLists.js";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  import { initialCode } from "$lib/initialCode.js";
  import { extractInteger } from "$lib/extractInteger.js";

  // Create variable for the historical code and states
  let keys = writable([]);
  let code = $state("");
  let counter = $state(1);
  let actualCode = $derived("Code-" + String(counter));

  let file = null;
  let isDarkMode = $state(false);
  let editorMode = $state(false);
  let pyscriptReady = $state(false);

  // Create a new list with the first unsorted list
  selectedList.set([...unsortedLists[0].value]);

  // Check the selectedList
  console.assert(
    selectedList !== undefined || selectedList !== null,
    "selectedList is undefined or null",
  );
  console.assert(
    Array.isArray(get(selectedList)),
    "selectedList is not an array",
  );

  // Check the unsortedLists
  console.assert(
    unsortedLists !== undefined || selectedList !== null,
    "unsortedLists is undefined",
  );
  console.assert(Array.isArray(unsortedLists), "unsortedLists is not an array");
  unsortedLists.forEach((list) => {
    console.assert(list.name !== undefined, "list.name is undefined");
    console.assert(list.value !== undefined, "list.value is undefined");
    console.assert(Array.isArray(list.value), "list.value is not an array");
    list.value.forEach((val, i) => {
      console.assert(typeof val === "number",`list.value[${i}] is not a number`,);
    });
  });

  /**
   * Sync the code with the localStorage
   * @returns {Function} - The interval function
   * @note - The interval function is used to sync the code with the localStorage, every 2 seconds
   */
  function syncCodeWithLocalStorage() {
    if (localStorage.getItem(actualCode) !== null) {
      code = localStorage.getItem(actualCode);
      window.selectLocalStorageStats();
    };

    const interval = setInterval(() => {
      code = updateCodeFromComponent();
      localStorage.setItem(actualCode, code);
      keys.set(Object.keys(localStorage));
    }, 2000);

    return () => clearInterval(interval);
  }

  /**
   * onMount function, executed when the component is mounted
   */
  onMount(() => {

    /**
     * Check if the browser is Safari
     * source : https://stackoverflow.com/a/23522755
    */
    if (/^((?!chrome|android).)*safari/i.test(navigator.userAgent)) {
      alert(
        "This website may not work optimally on Safari or any WebKit-based browser (such as Chrome or Firefox on iOS). You may experience slower performance or occasional freezes. For the best experience, use Google Chrome, Arc, or Firefox on a desktop.",
      );
      // Set the pyscriptReady to true, to enable the execution of the Python script on WebKit-based browsers
      pyscriptReady = true;
    }

    /**
     * Subscribe to the ready event of pyscript, to enable execution of the Python script
    */
    window.addEventListener("py:ready", () => {
      pyscriptReady = true;
    });

    /**
     * Assign variables to the dark mode and editor mode
     */
    const mode = window.matchMedia("(prefers-color-scheme: dark)");
    isDarkMode = mode.matches;
    editorMode = isDarkMode;
    /**
     * Listen to the change event of the dark mode
     * @param {Event} e - The change event
    */
    mode.addEventListener("change", (e) => {
      isDarkMode = e.matches;
      editorMode = isDarkMode;
    });

    /**
     * Sync the code with the localStorage, every 2 seconds
    */
    keys.set(Object.keys(localStorage));
    syncCodeWithLocalStorage();
  });

  /**
   * Handle the file change event
   * @param {Event} event - The file change event
   */
  function handleFileChange(event) {
    const selectedFile = event.target.files[0] || null;
    file = selectedFile;

    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        code = e.target.result;
      };
      reader.readAsText(file);
    } else {
      code = "";
    }
  }

  /**
   * Update the code from the component
   * @returns {String} - The updated code
   */
  function updateCodeFromComponent() {
    if (window === undefined) {
      return code;
    } else {
      window.updateEditorWindow();
      code = window.code;
      return code;
    }
  }

  /**
   * Delete the localStorage
   * @param {string} key - The key to delete
   */
  function deleteLocalStorage(key) {
    localStorage.removeItem(key);
    window.deleteStats(key);
    keys.set(Object.keys(localStorage));
  }

  /**
   * Add the localStorage
   * @note - The localStorage is added with the initial code
   */
  function addLocalStorage(){
    while (localStorage.getItem(actualCode) !== null) {
      counter++;
    }
    code = initialCode;
    syncCodeWithLocalStorage();
    window.addStats();
  }

  /**
   * Select the localStorage
   * @param {string} key - The key to select
   */
  function selectLocalStorage(key) {
    // update the counter variable
    counter = extractInteger(key);

    // update the actual code variable
    code = localStorage.getItem(actualCode);
    window.selectLocalStorageStats();
    window.resetGrid();
  }

  /**
   * Download the code
   * @note - The code is downloaded as a .py file, named "show-my-sort.py"
   */
  function downloadCode() {
    code = updateCodeFromComponent();

    // Code from https://stackoverflow.com/a/18197341, provided by GitHub Copilot
    const blob = new Blob([code], { type: "text/plain" });
    const elem = document.createElement("a");
    elem.href = URL.createObjectURL(blob);
    elem.download = "show-my-sort.py";
    elem.click();
    URL.revokeObjectURL(url);
  }
</script>

<main>
  <div class="navbar bg-base-100">
    <div class="navbar-start">
      <div class="dropdown">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h7"
            />
          </svg>
        </div>
        <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
        <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1000] mt-3 w-64 p-2 shadow">

            <!-- Sorting code from  Github Copilot-->
            {#each $keys.sort((a, b) => { const numA = parseInt(a.replace(/\D/g, ''), 10); const numB = parseInt(b.replace(/\D/g, ''), 10); return numA - numB;}) as key}
              {#if key.includes('Code')}
                <div class="grid grid-cols-5 items-center hover:bg-base-200 rounded p-1" class:bg-base-200={key == actualCode}>
                  <button class="btn btn-ghost col-span-4" onclick={() => selectLocalStorage(key)}>
                    <p class="text-sm lg:text-md font-medium ml-2">{key}</p>
                  </button>
                  
                  {#if !(key === actualCode)}
                    <button class="col-span-1 btn btn-ghost ml-auto p-3" id={key} aria-label="delete the code link to {key}" onclick={() => deleteLocalStorage(key)}>
                      <svg fill={isDarkMode ? "white" : 'black'} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="15" height="15">
                        <path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"/>
                      </svg>
                    </button>
                  {/if}
                </div>
              {/if}
            {/each}
            <div class="grid grid-cols-2 items-center rounded p-1">
              <button class="btn btn-ghost p-3" aria-label="Add a new code" onclick={() => addLocalStorage()}>
                <svg fill={isDarkMode ? "white" : 'black'} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="15" height="15">
                  <path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 144L48 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l144 0 0 144c0 17.7 14.3 32 32 32s32-14.3 32-32l0-144 144 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-144 0 0-144z"/>
                </svg>
              </button>
              <button class="btn btn-ghost bg-red-500 hover:bg-red-700 p-3" aria-label="delete all code stored in the localStorage" onclick={() => { localStorage.clear(); location.reload(); }}>
                <svg fill="white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="15" height="15">
                  <path d="M463.5 224l8.5 0c13.3 0 24-10.7 24-24l0-128c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1c-87.5 87.5-87.5 229.3 0 316.8s229.3 87.5 316.8 0c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0c-62.5 62.5-163.8 62.5-226.3 0s-62.5-163.8 0-226.3c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8l119.5 0z"/>
                </svg>
              </button>
            </div>
        </ul>
      </div>
    </div>
    <div class="navbar-center">
      <h1 class="text-2xl lg:text-4xl font-bold">Show My Sort</h1>
    </div>
    <div class="navbar-end flex justify-end">
      <label
        for="file-input"
        class="btn btn-ghost btn-circle"
        aria-label="Upload a file"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="20"
          width="20"
          viewBox="0 0 576 512"
        >
          <path
            fill={isDarkMode ? "white" : "black"}
            d="M128 64c0-35.3 28.7-64 64-64L352 0l0 128c0 17.7 14.3 32 32 32l128 0 0 288c0 35.3-28.7 64-64 64l-256 0c-35.3 0-64-28.7-64-64l0-112 174.1 0-39 39c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l80-80c9.4-9.4 9.4-24.6 0-33.9l-80-80c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l39 39L128 288l0-224zm0 224l0 48L24 336c-13.3 0-24-10.7-24-24s10.7-24 24-24l104 0zM512 128l-128 0L384 0 512 128z"
          />
        </svg>
        <input
          id="file-input"
          type="file"
          accept=".py"
          class="hidden"
          onchange={handleFileChange}
        />
      </label>

      <label
        for="file-output"
        class="btn btn-ghost btn-circle"
        aria-label="Download the code"
      >
        <button
          class="btn btn-ghost btn-circle"
          onclick={downloadCode}
          aria-label="Download the code"
        >
          <svg
            fill={isDarkMode ? "white" : "black"}
            xmlns="http://www.w3.org/2000/svg"
            height="20"
            width="20"
            viewBox="0 0 576 512"
          >
            <path
              d="M0 64C0 28.7 28.7 0 64 0L224 0l0 128c0 17.7 14.3 32 32 32l128 0 0 128-168 0c-13.3 0-24 10.7-24 24s10.7 24 24 24l168 0 0 112c0 35.3-28.7 64-64 64L64 512c-35.3 0-64-28.7-64-64L0 64zM384 336l0-48 110.1 0-39-39c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l80 80c9.4 9.4 9.4 24.6 0 33.9l-80 80c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l39-39L384 336zm0-208l-128 0L256 0 384 128z"
            />
          </svg>
        </button>
      </label>

      <label class="btn btn-ghost btn-circle">
        <label class="swap swap-rotate">
          <!-- this hidden checkbox controls the state -->
          <input
            type="checkbox"
            class="theme-controller"
            bind:checked={editorMode}
          />

          <!-- sun icon -->
          <svg
            class="swap-off h-8 w-8 fill-current"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
          >
            <path
              d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"
            />
          </svg>

          <!-- moon icon -->
          <svg
            class="swap-on h-8 w-8 fill-current"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
          >
            <path
              d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"
            />
          </svg>
        </label>
      </label>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4 ml-4 mr-4">
    <div
      class="grid p-2"
      style="border: 0.5px solid #000; border-radius: 15px;"
    >
      <Editor {code} {editorMode} {actualCode}/>
    </div>
    <div
      class="grid p-2"
      style="border: 0.5px solid #000; border-radius: 15px;"
    >
      <Diagram {unsortedLists} {isDarkMode} {pyscriptReady} {actualCode}/>
    </div>
  </div>

  <div class="flex flex-col items-center justify-center mt-8 mb-8">
    <div
      id="outputDiv"
      class="bg-base-200 p-4 rounded-lg shadow-lg w-full max-w-2xl"
    >
      <p id="output" class="text-lg text-center">
        {#if pyscriptReady}
          Execution states will be displayed here
        {:else}
          Python script is not ready
        {/if}
      </p>
    </div>
  </div>
</main>


<footer class="footer footer-center bg-base-200 text-base-content rounded p-10">
  <nav class="grid grid-flow-col gap-4 justify-between w-full">
    <div class="grid grid-cols-1">
      <button class="btn btn-ghost">
        <a
          href="mailto:florian.stormacq@student.unamur.be"
          class="flex items-center space-x-1"
        >
          <svg
            fill={isDarkMode ? "white" : "black"}
            xmlns="http://www.w3.org/2000/svg"
            height="20"
            width="20"
            viewBox="0 0 512 512"
          >
            <path
              d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48L48 64zM0 176L0 384c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-208L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z"
            />
          </svg>
          <span class="whitespace-nowrap"> Report an issue</span>
        </a>
      </button>

      <button class="btn btn-ghost">
        <a
          href="https://researchportal.unamur.be/fr/persons/slejoly"
          target="_blank"
          class="flex items-center space-x-1"
        >
          <svg
            fill={isDarkMode ? "white" : "black"}
            xmlns="http://www.w3.org/2000/svg"
            height="20"
            width="20"
            viewBox="0 0 512 512"
          >
            <path
              d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512l388.6 0c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304l-91.4 0z"
            />
          </svg>
          <span class="whitespace-nowrap">About my client</span>
        </a>
      </button>
    </div>

    <button class="btn btn-ghost">
      <a
        href="https://unamur.be"
        target="_blank"
        aria-label="UNamur website"
        class="flex items-center"
      >
        <img src="/logo/UNamur-vertical.svg" alt="UNamur logo" class="w-40" />
      </a>
    </button>
  </nav>
</footer>
