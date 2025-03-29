import ast

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