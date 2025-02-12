import ast

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