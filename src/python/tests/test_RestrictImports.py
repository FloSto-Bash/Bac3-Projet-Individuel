import unittest
import ast

from project.src.python.RestrictImports import RestrictImports

class TestRestrictImports(unittest.TestCase):
    
    # Test cases for visit_Import
    def test_invalid_import(self):
        '''
        Test case for invalid import
        
        Parameters:
        -----------
        self : TestRestrictImports (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        module = 'os'
        visitor = RestrictImports()
        import_node = ast.Import(names=[ast.alias(name=module, asname=None)])
        
        with self.assertRaises(Exception) as context:
            visitor.visit_Import(import_node)
        
        self.assertEqual(str(context.exception), f"Importing '{module}' module is not allowed")
        
    def test_valid_import(self):
        '''
        Test case for valid import
        
        Parameters:
        -----------
        self : TestRestrictImports (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        module = 'random'
        visitor = RestrictImports()
        import_node = ast.Import(names=[ast.alias(name=module, asname=None)])
        
        visitor.visit_Import(import_node)
        
    # Test cases for visit_ImportFrom
    def test_invalid_import_from(self):
        '''
        Test case for invalid import with the 'from' clause
        
        Parameters:
        -----------
        self : TestRestrictImports (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        module = 'os'
        visitor = RestrictImports()
        import_from_node = ast.ImportFrom(
            module=module, 
            names=[ast.alias(name='getcwd', asname=None)],
            level=0
        )
        
        with self.assertRaises(Exception) as context:
            visitor.visit_ImportFrom(import_from_node)
        
        self.assertEqual(str(context.exception), f"Importing from '{module}' module is not allowed")
        
    def test_valid_import_from(self):
        '''
        Test case for valid import with the 'from' clause
        
        Parameters:
        -----------
        self : TestRestrictImports (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        module = 'random'
        visitor = RestrictImports()
        import_from_node = ast.ImportFrom(
            module=module, 
            names=[ast.alias(name='randint', asname=None)], 
            level=0
        )
        
        visitor.visit_ImportFrom(import_from_node)
        
    # Test cases for visit_Attribute
    def test_invalid_attribute(self):
        '''
        Test case for invalid attribute
        
        Parameters:
        -----------
        self : TestRestrictImports (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        module = 'os'
        visitor = RestrictImports()
        attribute_node = ast.Attribute(
            value=ast.Name(id=module, ctx=ast.Load()), 
            attr='getcwd', 
            ctx=ast.Load()
        )
        
        with self.assertRaises(Exception) as context:
            visitor.visit_Attribute(attribute_node)
        
        self.assertEqual(str(context.exception), f"Access to '{module}' module is not allowed")
        
    def test_valid_attribute(self):
        '''
        Test case for valid attribute
        
        Parameters:
        -----------
        self : TestRestrictImports (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        module = 'random'
        visitor = RestrictImports()
        attribute_node = ast.Attribute(
            value=ast.Name(id=module, ctx=ast.Load()), 
            attr='randint', 
            ctx=ast.Load()
        )
        
        visitor.visit_Attribute(attribute_node)

if __name__ == '__main__':
    unittest.main()