import ast

# Liste des modules restreints
RESTRICTED_MODULES = {'os', 'sys', 'subprocess', 'shutil', 'socket', 'http', 'ftplib', 'pickle'}
RESTRICTED_VARIABLES = {'myList'}

def check_import(node):
    '''
    Vérifie les imports pour restreindre certains modules
    
    Parameters:
    -----------
    node: ast.Import
    
    Raises:
    -------
    Exception: Si un module restreint est importé
    '''
    assert hasattr(node, 'names') and isinstance(node.names, list), "Node does not have 'names' attribute or it is not a list"
    for alias in node.names:
        if alias.name in RESTRICTED_MODULES:
            raise Exception(f"Importing '{alias.name}' module is not allowed")

def check_import_from(node):
    '''
    Vérifie les imports "from ... import ..." pour restreindre certains modules
    
    Parameters:
    -----------
    node: ast.ImportFrom
    
    Raises:
    -------
    Exception: Si un module restreint est importé
    '''
    assert hasattr(node, 'module'), "Node does not have 'module' attribute"
    if node.module in RESTRICTED_MODULES:
        raise Exception(f"Importing from '{node.module}' module is not allowed")

def check_attribute(node):
    '''
    Vérifie l'accès aux modules restreints via des attributs
    
    Parameters:
    -----------
    node: ast.Attribute
    
    Raises:
    -------
    Exception: Si un module restreint est accédé
    '''
    assert hasattr(node, 'value'), "Node does not have 'value' attribute"
    if isinstance(node.value, ast.Name) and node.value.id in RESTRICTED_MODULES:
        raise Exception(f"Access to '{node.value.id}' module is not allowed")

def check_variable_redefinition(node):
    '''
    Vérifie la redéfinition de certaines variables
    
    Parameters:
    -----------
    node: ast.Assign
    
    Raises:
    -------
    Exception: Si une variable restreinte est redéfinie
    '''
    assert hasattr(node, 'targets') and isinstance(node.targets, list), "Node does not have 'targets' attribute or it is not a list"
    for target in node.targets:
        if isinstance(target, ast.Name) and target.id in RESTRICTED_VARIABLES:
            raise Exception(f"Redefining '{target.id}' variable is not allowed")
  
def check_node(node):
    '''
    Vérifie les imports et l'accès aux modules restreints
    
    Parameters:
    -----------
    node: ast.Module
    
    Raises:
    -------
    Exception: Si un module restreint est importé ou accédé
    '''
    assert hasattr(node, 'body') and isinstance(node.body, list), "Node does not have 'body' attribute or it is not a list"
    for child in node.body:
        if isinstance(child, ast.Import):
            check_import(child)
        elif isinstance(child, ast.ImportFrom):
            check_import_from(child)
        elif isinstance(child, ast.Attribute):
            check_attribute(child)
        elif isinstance(child, ast.Assign):
            check_variable_redefinition(child)