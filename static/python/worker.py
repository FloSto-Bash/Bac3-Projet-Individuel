from pyscript import document, sync # type: ignore
from time import time, sleep
import pyodide # type: ignore
# from restricted.RestrictImports import RestrictImports # Temporary : this import is not working, so the class is copied below
# from restricted.RestrictVariableRedefinition import RestrictVariableRedefinition # Temporary : this import is not working, so the class is copied below

import ast, copy

timedExecution = False
swapCount = 0
compareCount = 0

class RestrictImports(ast.NodeVisitor):
    '''
    Author: GitHub Copilot
    
    This class restricts the use of certain modules in the code
    '''
    
    # Restricted modules, can be modified as needed
    restricted_modules = {'os', 'sys', 'subprocess', 'shutil', 'socket', 'http', 'ftplib', 'pickle'}

    def visit_Import(self, node):
        '''
        Restricts the use of certain modules in the code, when trying to import them
        
        Parameters:
        -----------
        self: RestrictImports (class)
        node: ast.Import 
        
        Raises:
        -------
        Exception: If the module being imported in a 'import' statement is restricted
        '''
        assert hasattr(node, 'names') and isinstance(node.names, list), "Node does not have 'names' attribute or it is not a list"
        for alias in node.names:
            if alias.name in self.restricted_modules:
                raise Exception(f"Importing '{alias.name}' module is not allowed")
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        '''
        Restricts the use of certain modules in the code, when trying to import them using 'from'
        
        Parameters:
        -----------
        self: RestrictImports (class)
        node: ast.ImportFrom
        
        Raises:
        -------
        Exception: If the module being importedin a 'from' statement is restricted 
        '''
        assert hasattr(node, 'module'), "Node does not have 'module' attribute"
        if node.module in self.restricted_modules:
            raise Exception(f"Importing from '{node.module}' module is not allowed")
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        '''
        Restricts the use of certain modules in the code, when trying to access them
        
        Parameters:
        -----------
        self: RestrictImports (class)
        node: ast.Attribute
        
        Raises:
        -------
        Exception: If the module being accessed in an 'attribute' statement is restricted
        '''
        assert hasattr(node, 'value'), "Node does not have 'value' attribute"
        if isinstance(node.value, ast.Name) and node.value.id in self.restricted_modules:
            raise Exception(f"Access to '{node.value.id}' module is not allowed")
        self.generic_visit(node)
             
class RestrictVariableRedefinition(ast.NodeVisitor):
    '''
    Author: GitHub Copilot
    
    This class restricts the redefinition of certain variables in the code
    
    Note:
    ------
    This class is not used in the current implementation
    '''
    
    # Restricted variables, can be modified as needed
    restricted_variables = {'myList'}

    def visit_Assign(self, node):
        '''
        Restricts the redefinition of certain variables in the code
        
        Parameters:
        -----------
        self: RestrictVariableRedefinition (class)
        node: ast.Assign
        
        Raises:
        -------
        Exception: If the variable being redefined is restricted
        '''
        assert hasattr(node, 'targets') and isinstance(node.targets, list), "Node does not have 'targets' attribute or it is not a list"
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in self.restricted_variables:
                raise Exception(f"Redefining '{target.id}' variable is not allowed")
        self.generic_visit(node)

def parse_and_restrict(code: str):
    '''
    Parses the code and restricts the imports and variable redefinitions
    
    Parameters:
    -----------
    code: The code entered by the user in the editor (str)
    
    Return:
    -------
    parsed_code: The parsed code after restricting the imports and variable redefinitions (ast.Module)
    
    Notes:
    ------
    Exception: If an error occurs during the parsing of the code
    '''
    parsed_code = ast.parse(code, mode='exec')
    RestrictImports().visit(parsed_code)
    RestrictVariableRedefinition().visit(parsed_code)
    return parsed_code
  
def compare(arr : list, i : int, j : int) -> bool:
    '''
    Compares two integers, returns True if arr[i] is less than or equal to arr[j], False otherwise
    
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
    assert isinstance(arr, list), f"Expected list, got {type(arr)}"
    assert isinstance(arr[i], int), f"Expected int, got {type(arr[i])}"
    assert isinstance(arr[j], int), f"Expected int, got {type(arr[j])}"


    if sync.getCompare() and not timedExecution:
        sync.compareOnDiagram(i, j)
        sleep(sync.getAnimationTime()/10_000)
        
    updateCompareCount()
    
    return arr[i] <= arr[j]

def swap(arr : list, i : int, j : int):
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
    assert arr != [], "List is empty"
    assert i < len(arr), "Index out of range"
    assert j < len(arr), "Index out of range"

    arr[i], arr[j] = arr[j], arr[i]
    
    # convert the list to a JsProxy object before updating the list in the front-end
    sync.updateList(pyodide.ffi.to_js(arr), i, j, timedExecution)
    updateSwapCount() 
    
    if sync.getSwap() and not timedExecution:
        sleep(sync.getAnimationTime()/1_000)
        
        
def defineGlobals(myList) -> dict:
    '''
    Defines the global variables and builtins functions that can be accessed by the user's code
    
    Parameter:
    ----------
    myList: The list currently selected by the user (pyodide.ffi.JsProxy)
    
    Return:
    -------
    exec_globals: The global variables and builtins functions that can be accessed by the user's code (dict)
    '''
    # Convert JsProxy to a native Python list
    if isinstance(myList, pyodide.ffi.JsProxy):
        myList = list(myList)
    
    assert all(isinstance(i, int) for i in myList), "All elements of the list should be integers"
    assert len(myList) > 0, "List should not be empty"
    
    assert callable(compare), f"Expected callable, got {type(compare)}"
    assert callable(swap), f"Expected callable, got {type(swap)}"
    
    exec_globals = {
        '__builtins__': {
            '__import__' : __import__,
            'print': print,
            'range': range,
            'len': len,
            'int': int,
            'float': float,
            'str': str,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'bool': bool,
            'type': type,
            'Exception': Exception,
            'min': min,
            'max': max,
            'enumerate': enumerate,
            'all' : all,
            'any' : any,
            'abs' : abs,
            'sum' : sum,
            'reversed' : reversed,
            'round' : round
        },
        'myList':  copy.deepcopy(myList),
        'compare' : compare,
        'swap' : swap
    }
    
    return exec_globals

def execute_code(code, myList, measuringTime = False):
    '''
    Executes the user's code and returns the result
    
    Parameters:
    -----------
    code: The code entered by the user in the editor (str)
    myList: The list currently selected by the user (pyodide.ffi.JsProxy)
    
    Return:
    -------
    myList: The list after the code has been executed
    
    Raises:
    -------
    Exception: If an error occurs during the execution of the code
    '''
    updateCompareCount(reset=True)
    updateSwapCount(reset=True)
    
    assert isinstance(code, str), f"Expected str, got {type(code)}"
    
    outputDiv = document.getElementById('output')
    assert outputDiv is not None, "Output div not found"
    
    if not measuringTime :
        outputDiv.innerHTML = "Executing code..."
    
    exec_globals = defineGlobals(myList)
    assert exec_globals is not None, "Global variables not defined"


    # The 'ast' module is used to parse the code and restrict the imports and variable redefinitions
    parsed_code = parse_and_restrict(code)
    
    if measuringTime :
        global timedExecution
        timedExecution = True
        start_time = time()
    
    compiled_code = compile(parsed_code, filename='', mode='exec')
    
    exec(compiled_code, exec_globals)
    
    if measuringTime :
        timedExecution = False
        end_time = time()
        final_time = end_time - start_time
    
    myList = exec_globals.get('myList')
    
    if myList is None:
        outputDiv.innerHTML = "Something went wrong... please try again"
        raise Exception("List is None")
    else :
        if not measuringTime :
            outputDiv.innerHTML = "Code executed successfully"
    
    if measuringTime :
        sync.updateCompareCount(compareCount)
        sync.updateSwapCount(swapCount)
        return final_time
    
    return pyodide.ffi.to_js(myList)

def updateSwapCount(reset = False) -> None:
    '''
    Updates the swap count
    '''
    global swapCount
    if reset :
        swapCount = 0
    else :
        swapCount += 1
    
def updateCompareCount(reset = False) -> None:
    '''
    Updates the compare count
    '''
    global compareCount
    if reset :
        compareCount = 0
    else : 
        compareCount += 1
      
# The 'sync' object is used to communicate with the main thread
sync.execute_code = execute_code