# Show My Sort : documentation

## Project Overview
This project was realized as part of the course "Projet inidividuel" at the University of Namur, during the academic year 2024-2025.
The project is a web application that allows users to code sorting algorithms in Python and visualize their execution in real-time. The application is built using PyScript, a framework that allows Python code to run in the browser.

## Project Structure
```bash
project/
├── ...
├── .svelte-kit/
│   ├── ...
├── src/
│   ├── app.css
│   ├── app.html
│   ├── lib/
│   │   ├── ...
│   ├── routes/
│   │   ├── ...
│   │   ├── +page.svelte
│   │   └── components/
│   │       ├── diagram.svelte
│   │       └── editor.svelte
├── static/
│   ├── icon/
│   ├── logo/
│   ├── python/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── restricted_checks.py
│   │   │   ├── worker.py
│   │   └── config/
│   │       └── pyscript.json

```

## Main dependencies
- [PyScript](https://pyscript.net/)
- [Svelte](https://svelte.dev/)
- [Monaco Editor](https://microsoft.github.io/monaco-editor/)

## Installation
To run the project locally, please follow these steps:

1. Ensure to be in the root directory of the project. If it is not the case, you are probably in the 'SMS-01' directory. In this case, please run the following command:
```bash
cd project
```
2. Install the dependencies:
```bash
npm install
```
3. Start the development server:
```bash
npm run dev
```
4. Open your browser and navigate to `http://localhost:5173/`, or click on the link provided in the terminal.
5. You can now start coding and visualizing sorting algorithms in Python!

## Usage
Show My Sort is a reactive web application, that allows users to code sorting algorithms in Python and visualize their execution in real-time. The application provides :

- A code editor powered by Monaco Editor, which supports syntax highlighting and auto-completion.
- A diagram that visualizes the sorting process in real-time.
- Customizable parameters for the sorting algorithms, such as the array to sort, the speed of the visualization, visualization of comparisons and swaps and statistics.
- A console that displays the state of the running code, including error messages.
- A button to reset the grid, run the code and reset the statistics.
- Buttons to download the code and upload a new one.
- A local storage feature that saves the code and statistics, so you can continue where you left off.
- A light/dark mode.
- The possibility for the user to choose the light/dark mode of the editor independently of the application.

## Known Issues
Despite the fact that the application is fully functional, some issues have been identified. They are listed below:

1. Issue on iPadOS devices, with the upper version of pyodide 0.27.0. The error message is `RangeError: Maximum call stack size exceeded`. This issue is not present on other devices. See [interpreter-explanation.md](static/python/config/interpreter-explaination.md) for more details.
2. If you have played a little with the application, you may have seen the following message in the output console : "Something went wrong... please try again". This message indicates that an error occured during the execution of the code. Such errors are not due to the application's code, but rather to the parsing of JSON content. It can only be minimized, but not completely avoided. 

## Contacts
Please feel free to contact me if you have any questions, suggestions, or issues. You can use the contact button available on the web application for this purpose.

## License
This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.