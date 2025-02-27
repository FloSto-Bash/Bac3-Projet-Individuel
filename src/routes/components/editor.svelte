<script>
    import { onMount } from "svelte";
    import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
    import { selectedList } from "$lib/selectedList.js";
    import { initialCode } from "$lib/initialCode.js";

    let myList;
    let subscriptions = [];
    let content;
    let divEl;
    let editor;
    let Monaco;

    let { code, editorMode, actualCode } = $props();

    /**
     * Subscribe to the selected list
     */
    const unsubscribe = selectedList.subscribe(value => {
        myList = value;
        if (typeof window !== 'undefined') {
            window.myList = myList;
        }
    });

    /**
     * Update the dimensions of the editor
     */
    function updateEditorDimensions() {
        let width;
        let height;
        const gridElement = divEl.closest('.grid');
        width = gridElement.clientWidth * 0.98;
        
        // review this to avoid a loading image issue
        if (window.innerWidth > 1024) {
            height = window.innerHeight * 0.73;
        } else {
            height = window.innerHeight * 0.48;
        }

        if (height < 478 * 0.98) {
            height = 478 * 0.98;
        }
        
        console.assert(width !== undefined || height !== undefined, 'width or height is undefined');
        console.assert(typeof width === 'number' || typeof height === 'number', 'width or height is not a number');

        console.assert(divEl !== undefined, 'divEl is undefined');
        divEl.style.width = `${width}px`;
        divEl.style.height = `${height}px`;
        if (editor) {
            editor.layout();
            editor.updateOptions({
                fontSize: window.innerWidth > 1024 ? 14 : 12
            });
        }
    }

    /**
     * Initialise the editor
     */
    onMount(async () => {
        /**
         * Set up the Monaco environment
         * @author github Copilot
         */
        self.MonacoEnvironment = {
            getWorker: function (_moduleId, label) {
                return new editorWorker();
            },
        };
        Monaco = await import("monaco-editor");

        // Check the div element and initial code
        console.assert(divEl !== undefined, 'divEl is undefined');
        console.assert(initialCode !== undefined, 'initialCode is undefined');
        console.assert(typeof initialCode === 'string', 'initialCode is not a string');

        // Creates the Monaco editor
        editor = Monaco.editor.create(divEl, {
            value: localStorage.getItem(actualCode) === null ? initialCode : localStorage.getItem(actualCode),
            language: "python",
            theme: editorMode ? "vs-dark" : "vs-light",
            readOnly: false,
            fontSize: window.innerWidth > 1024 ? 14 : 12,
        });

        /**
         * Subscribe to changes in the editor
         */
        editor.onDidChangeModelContent(() => {
            const text = editor.getValue();
            subscriptions.forEach((sub) => sub(text));
        });
        content = {
            subscribe(func) {
                subscriptions.push(func);
                return () => {
                    subscriptions = subscriptions.filter((sub) => sub != func);
                };
            },
            set(val) {
                editor.setValue(val);
            },
        };

        code = editor.getValue();

        // Check the window, editor, and myList
        console.assert(window !== undefined, 'onMount : window is undefined');
        console.assert(editor !== undefined, 'onMount : editor is undefined');
        console.assert(myList !== undefined, 'onMount : myList is undefined');

        window.editor = editor;
        window.myList = myList;
        window.updateEditorWindow = () =>  {window.code = editor.getValue()};
        window.updateList = updateList;

        updateEditorDimensions();

        // Update the editor dimensions when the window is resized
        window.addEventListener('resize', updateEditorDimensions);

        // Clean up subscription and event listener when component is destroyed
        return () => {
            unsubscribe();
            window.removeEventListener('resize', updateEditorDimensions);
        };
    });

    /**
     * Update the list
     * @param {Array} arr - The new list
     */
    async function updateList(arr){ 
        console.assert(arr !== undefined, 'updateList : arr is undefined');
        console.assert(Array.isArray(arr), 'updateList : arr is not an array');
        selectedList.set(arr);
    }

    /**
     * Update the editor with the new code
     */
    $effect (() => {
        if (code !== undefined && editor !== undefined) {
            const position = editor.getPosition();
            editor.setValue(code);
            editor.setPosition(position);
        }
    });

    /**
     * Update the editor theme
     */
    $effect (() => {
        if (editorMode !== undefined && editor !== undefined) {
            editor.updateOptions({ theme: editorMode ? "vs-dark" : "vs-light" });
        }
    });
</script>

<div id="editor" bind:this={divEl}></div>