from pyscript import document, sync       # type: ignore
from time import time, sleep
from js import postMessage                # type: ignore
import pyodide, copy, ast                 # type: ignore

# from restricted_checks import check_node
# This import does not work for some reason. The functions from the restricted_checks module are copied below
# However, I respected the pyscript documentation relative to the configuration.
# See : https://docs.pyscript.net/2025.3.1/user-guide/configuration/#files

timedExecution = False
swapCount = 0
compareCount = 0

def parse_and_restrict(code: str) -> ast.Module:
    '''
    Parses the code and restricts the imports and variable redefinitions.
    
    Parameters:
    -----------
    code: The code entered by the user in the editor (str)
    
    Return:
    -------
    parsed_code: The parsed code after restricting the imports and variable redefinitions (ast.Module)
    
    Notes:
    ------
    Exception: If an error occurs during restricting the imports and variable redefinitions
    '''
    assert isinstance(code, str), f"Expected str, got {type(code)}, in parse_and_restrict"
    
    parsed_code = ast.parse(code, mode='exec')
    check_node(parsed_code)
    return parsed_code
  
def compare(arr : list, i : int, j : int) -> bool:
    '''
    Compares two integers, returns True if arr[i] is less than or equal to arr[j], False otherwise.
    
    Parameters:
    -----------
    arr: The list in which the elements are to be compared (list)
    i: The index of the first integer (int)
    j: The index of the second integer (int)
    
    Return:
    -------
    result: True if arr[i] is less than or equal to arr[j], False otherwise (bool)
    
    Note:
    ------
    This function is available to the user's code
    '''
    assert isinstance(arr, list), f"Expected list, got {type(arr)}, in compare"
    assert len(arr) > 0, "List should not be empty, in compare"
    
    assert isinstance(i, int) and not isinstance(i, bool), f"Expected int, got {type(i)}, in compare"
    assert i < len(arr), f"Index {i} out of range, in compare"
    assert i >= 0, f"Index {i} out of range, in compare"
    
    assert isinstance(j, int) and not isinstance(i, bool), f"Expected int, got {type(j)}, in compare"
    assert j < len(arr), f"Index {j} out of range, in compare"
    assert j >= 0, f"Index {j} out of range, in compare"
    

    assert callable(sync.compareOnDiagram), f"Expected callable, got {type(sync.compareOnDiagram)}, in compare"
    if sync.getCompare() and not timedExecution:
        sync.compareOnDiagram(i, j)
        sleep(sync.getAnimationTime() / 10_000)
        
    updateCompareCount()
    return arr[i] <= arr[j]

def updateCompareCount(reset=False) -> None:
    '''
    Updates the compare count
    
    Parameters:
    -----------
    reset: If True, the compare count is reset to 0 (bool)
    '''
    global compareCount
    if reset:
        compareCount = 0
    else:
        compareCount += 1

def swap(arr: list, i: int, j: int):
    '''
    Swaps the elements at the given indices in the list
    
    Parameters:
    -----------
    arr: The list in which the elements are to be swapped (list)
    i: The index of the first element (int)
    j: The index of the second element (int)
    
    Note:
    ------
    This function is available to the user's code
    '''    
    assert isinstance(arr, list), f"Expected list, got {type(arr)}, in swap"
    assert len(arr) > 0, "List should not be empty, in swap"
    
    assert isinstance(i, int) and not isinstance(i, bool), f"Expected int, got {type(i)}, in swap"
    assert i < len(arr), f"Index {i} out of range, in swap"
    assert i >= 0, f"Index {i} out of range, in swap"
    
    assert isinstance(j, int) and not isinstance(i, bool), f"Expected int, got {type(j)}, in swap"
    assert j < len(arr), f"Index {j} out of range, in swap"
    assert j >= 0, f"Index {j} out of range, in swap"

    arr[i], arr[j] = arr[j], arr[i]
    
    # Convert the list to a JsProxy object before updating the list in the front-end
    sync.updateList(pyodide.ffi.to_js(arr), i, j, timedExecution)
    updateSwapCount() 
    
    if sync.getSwap() and not timedExecution:
        sleep(sync.getAnimationTime() / 1_000)

def updateSwapCount(reset = False) -> None:
    '''
    Updates the swap count
    
    Parameters:
    -----------
        reset: If True, the swap count is reset to 0 (bool)
    '''
    global swapCount
    if reset :
        swapCount = 0
    else :
        swapCount += 1
        
        
def defineGlobals(myList) -> dict:
    '''
    Defines the global variables and builtins functions that can be accessed by the user's code
    
    Parameter:
    ----------
    myList: The list currently selected by the user (list)
    
    Return:
    -------
    exec_globals: The global variables and builtins functions that can be accessed by the user's code (dict)
    '''
    # Convert JsProxy to a native Python list
    if isinstance(myList, pyodide.ffi.JsProxy):
        myList = list(myList)
    
    assert isinstance(myList, list), f"Expected list, got {type(myList)}, in defineGlobals"
    assert all((isinstance(i, int) and not isinstance(i, bool)) for i in myList), "All elements of the list should be integers, in defineGlobals"
    assert len(myList) > 0, "List should not be empty, in defineGlobals"
    
    assert callable(compare), f"Expected callable, got {type(compare)}, in defineGlobals"
    assert callable(swap), f"Expected callable, got {type(swap)}, in defineGlobals"
    
    exec_globals = {
        '__builtins__': {
            '__import__': __import__,
            'range': range,
            'len': len,
            'int': int,
            'float': float,
            'str': str,
            'list': list,
            'bool': bool,
            'min': min,
            'max': max,
            'all': all,
            'any': any,
            'abs': abs,
            'sum': sum,
            'round': round,
            'reversed': reversed
        },
        'myList': copy.deepcopy(myList),
        'compare': compare,
        'swap': swap
    }
    
    return exec_globals

def execute_code(code, myList, measuringTime=False) -> list | float | None:
    '''
    Executes the user's code and returns the result
    
    Parameters:
    -----------
    code: The code entered by the user in the editor (str)
    myList: The list currently selected by the user (list)
    measuringTime: If True, the time taken to execute the code is returned (bool)
    
    Return:
    -------
    By default : myList: The list after the code has been executed 
    If measuringTime is True: final_time: The time taken to execute the code (float)
    If an error occurs: None
    
    Raises:
    -------
    Exception: If an error occurs during the execution of the code
    
    Note:
    -----
    The postMessage function is used to send the error to the main thread, where it handles the error
    '''
    assert isinstance(code, str), f"Expected str, got {type(code)}, in execute_code"
    
    # Handle the case when myList is not a list 
    if isinstance(myList, pyodide.ffi.JsProxy):
        myList = list(myList)
        
    assert isinstance(myList, list), f"Expected list, got {type(myList)}, in execute_code"
    assert all((isinstance(i, int) and not isinstance(i, bool)) for i in myList), "All elements of the list should be integers, in execute_code"
    assert len(myList) > 0, "List should not be empty, in execute_code"
    
    assert isinstance(measuringTime, bool), f"Expected bool, got {type(measuringTime)}, in execute_code"
    
    # Reset the compare and swap count for the new code execution
    updateCompareCount(reset=True)
    updateSwapCount(reset=True)
    
    assert isinstance(code, str), f"Expected str, got {type(code)}, in execute_code"
    
    outputDiv = document.getElementById('output')
    assert outputDiv is not None, "Output div not found, in execute_code"
    
    exec_globals = defineGlobals(myList)
    assert exec_globals is not None, "Global variables not defined, in execute_code"

    if not measuringTime:
        outputDiv.innerHTML = "Executing code..."
        
    # The 'ast' module is used to parse the code and restrict the imports and variable redefinitions
    try:
        parsed_code = parse_and_restrict(code)
    except Exception as e:
        # Handle the case when an error occurs during the parsing of the code
        postMessage(f"{str(e)}")
        return
    
    if measuringTime:
        global timedExecution
        timedExecution = True
        start_time = time()
    
    compiled_code = compile(parsed_code, filename='', mode='exec')
    
    try:
        exec(compiled_code, exec_globals)
    except Exception as e:
        # Handle the case when an error occurs during the execution of the code
        postMessage(f"{str(e)}")
        return
    
    if measuringTime:
        timedExecution = False
        end_time = time()
        final_time = end_time - start_time
        
        # Update the compare and swap count in the front-end
        sync.updateCompareCount(compareCount)
        sync.updateSwapCount(swapCount)
        return final_time
    
    myList = exec_globals.get('myList')
        
    if myList is None:
        # Handle the case when the list is not found
        postMessage("List not found")
        return

    outputDiv.innerHTML = "Code executed successfully"
    return myList
      
# The 'sync' object is used to communicate with the main thread
sync.execute_code = execute_code

# ------------------------------------------------------------------------------------------------------------------------
# The following classes are used to restrict the imports and variable redefinitions in the user's code. It has been copied
# in the current file. The classes were normally in a separate file (see ./static/python/src/restricted_checks.py), but 
# import problems with pyscript forced me to copy the classes in the current file.
# ------------------------------------------------------------------------------------------------------------------------

# List of restricted modules
RESTRICTED_MODULES = {'os', 'sys', 'subprocess', 'shutil', 'socket', 'http', 'ftplib', 'pickle'}
RESTRICTED_VARIABLES = {'myList'}

def check_import(node):
    '''
    Checks "import ..." to restrict some modules
    
    Parameters:
    -----------
    node: ast.Import
    
    Raises:
    -------
    Exception: If a restricted module is imported
    '''
    assert hasattr(node, 'names') and isinstance(node.names, list), "Node does not have 'names' attribute or it is not a list, in check_import"
    for alias in node.names:
        if alias.name in RESTRICTED_MODULES:
            raise Exception(f"Importing '{alias.name}' module is not allowed")

def check_import_from(node):
    '''
    Checks "from ... import ..." imports to restrict some modules
    
    Parameters:
    -----------
    node: ast.ImportFrom
    
    Raises:
    -------
    Exception: If a restricted module is imported
    '''
    assert hasattr(node, 'module'), "Node does not have 'module' attribute, in check_import_from"
    if node.module in RESTRICTED_MODULES:
        raise Exception(f"Importing from '{node.module}' module is not allowed")

def check_attribute(node):
    '''
    Checks access to restricted modules via attributes
    
    Parameters:
    -----------
    node: ast.Attribute
    
    Raises:
    -------
    Exception: If a restricted module is accessed
    '''
    assert hasattr(node, 'value'), "Node does not have 'value' attribute, in check_attribute"
    if isinstance(node.value, ast.Name) and node.value.id in RESTRICTED_MODULES:
        raise Exception(f"Access to '{node.value.id}' module is not allowed")

def check_variable_redefinition(node):
    '''
    Checks redefinition of certain variables
    
    Parameters:
    -----------
    node: ast.Assign
    
    Raises:
    -------
    Exception: If a restricted variable is redefined
    '''
    assert hasattr(node, 'targets') and isinstance(node.targets, list), "Node does not have 'targets' attribute or it is not a list, in check_variable_redefinition"
    for target in node.targets:
        if isinstance(target, ast.Name) and target.id in RESTRICTED_VARIABLES:
            raise Exception(f"Redefining '{target.id}' variable is not allowed")
  
def check_node(node):
    '''
    Checks the AST node for restricted imports, attributes, and variable redefinitions
    
    Parameters:
    -----------
    node: ast.Module
    
    Raises:
    -------
    Exception: If a restricted module is imported, accessed, or used in a call
    
    Note:
    -----
    This function traverses the AST node and its children to ensure that no restricted modules
    are imported, accessed, or used in a call. It also checks for redefinitions of certain variables.
    It raises an exception if any restricted module is found.
    '''
    assert hasattr(node, 'body') and isinstance(node.body, list), "Node does not have 'body' attribute or it is not a list, in check_node"
    for child in node.body:
        if isinstance(child, ast.Import):
            check_import(child)
        elif isinstance(child, ast.ImportFrom):
            check_import_from(child)
        elif isinstance(child, ast.Attribute):
            check_attribute(child)
        elif isinstance(child, ast.Assign):
            check_variable_redefinition(child)