import unittest

from project.src.python.RestrictVariableRedefinition import RestrictVariableRedefinition
import ast

class TestRestrictVariableRedefinition(unittest.TestCase):
    
    # Test cases for visit_Assign
    def test_invalid_assign(self):
        '''
        Test case for invalid assignment
        
        Parameters:
        -----------
        self : TestRestrictVariableRedefinition (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        visitor = RestrictVariableRedefinition()
        variable = 'myList'
        assign_node = ast.Assign(
            targets = [ast.Name(id = variable, ctx = ast.Store())], 
            value = [1, 2, 3]
        )
        
        with self.assertRaises(Exception) as context:
            visitor.visit_Assign(assign_node)
        
        self.assertEqual(str(context.exception), f"Redefining '{variable}' variable is not allowed")
        
    def test_valid_assign(self):
        '''
        Test case for valid assignment
        
        Parameters:
        -----------
        self : TestRestrictVariableRedefinition (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        visitor = RestrictVariableRedefinition()
        variable = 'b'
        assign_node = ast.Assign(
            targets=[ast.Name(id = variable, ctx = ast.Store())], 
            value=5
        )
        
        visitor.visit_Assign(assign_node)
        
    def test_multiple_assignments(self):
        '''
        Test case for multiple assignments
        
        Parameters:
        -----------
        self : TestRestrictVariableRedefinition (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        visitor = RestrictVariableRedefinition()
        assign_node = ast.Assign(
            targets=[ast.Name(id='a', ctx=ast.Store()), ast.Name(id='myList', ctx=ast.Store())], 
            value=5
        )
        
        with self.assertRaises(Exception) as context:
            visitor.visit_Assign(assign_node)
        
        self.assertEqual(str(context.exception), "Redefining 'myList' variable is not allowed")
    
