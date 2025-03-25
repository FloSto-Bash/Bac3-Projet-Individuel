import unittest
import ast

from ..src.restricted_checks import check_import, check_import_from, check_attribute, check_variable_redefinition

class TestRestrictImports(unittest.TestCase):
    
    # Test cases for check_import
    def test_invalid_import(self):
        '''
        Test case for invalid import
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        module = 'os'
        import_node = ast.Import(names=[ast.alias(name=module, asname=None)])
        
        with self.assertRaises(Exception) as context:
            check_import(import_node)
        
        self.assertEqual(str(context.exception), f"Importing '{module}' module is not allowed")
        
    def test_valid_import(self):
        '''
        Test case for valid import
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        module = 'random'
        import_node = ast.Import(names=[ast.alias(name=module, asname=None)])
        
        check_import(import_node)
        
    # Test cases for check_import_from
    def test_invalid_import_from(self):
        '''
        Test case for invalid import with the 'from' clause
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        module = 'os'
        import_from_node = ast.ImportFrom(
            module=module, 
            names=[ast.alias(name='getcwd', asname=None)],
            level=0
        )
        
        with self.assertRaises(Exception) as context:
            check_import_from(import_from_node)
        
        self.assertEqual(str(context.exception), f"Importing from '{module}' module is not allowed")
        
    def test_valid_import_from(self):
        '''
        Test case for valid import with the 'from' clause
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        module = 'random'
        import_from_node = ast.ImportFrom(
            module=module, 
            names=[ast.alias(name='randint', asname=None)], 
            level=0
        )
        
        check_import_from(import_from_node)
        
    # Test cases for check_attribute
    def test_invalid_attribute(self):
        '''
        Test case for invalid attribute
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        module = 'os'
        attribute_node = ast.Attribute(
            value=ast.Name(id=module, ctx=ast.Load()), 
            attr='getcwd', 
            ctx=ast.Load()
        )
        
        with self.assertRaises(Exception) as context:
            check_attribute(attribute_node)
        
        self.assertEqual(str(context.exception), f"Access to '{module}' module is not allowed")
        
    def test_valid_attribute(self):
        '''
        Test case for valid attribute
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        module = 'random'
        attribute_node = ast.Attribute(
            value=ast.Name(id=module, ctx=ast.Load()), 
            attr='randint', 
            ctx=ast.Load()
        )
        
        check_attribute(attribute_node)
    
    # Test cases for check_variable_redefinition
    def test_invalid_variable_redefinition(self):
        '''
        Test case for invalid variable redefinition
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        variable = 'myList'
        assign_node = ast.Assign(
            targets=[ast.Name(id=variable, ctx=ast.Store())],
            value=ast.List(elts=[], ctx=ast.Load())
        )
        
        with self.assertRaises(Exception) as context:
            check_variable_redefinition(assign_node)
        
        self.assertEqual(str(context.exception), f"Redefining '{variable}' variable is not allowed")
    
    def test_valid_variable_redefinition(self):
        '''
        Test case for valid variable redefinition
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        variable = 'myVariable'
        assign_node = ast.Assign(
            targets=[ast.Name(id=variable, ctx=ast.Store())],
            value=ast.List(elts=[], ctx=ast.Load())
        )
        
        check_variable_redefinition(assign_node)

if __name__ == '__main__':
    unittest.main()