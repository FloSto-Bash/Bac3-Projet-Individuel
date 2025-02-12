import unittest
from worker import execute_code, defineGlobals, swap, compare

# This test code does not work for the moment. The problem is that the document, window and sync objects are not defined in the test environment.
# Will try to find a solution to this problem after the exams.

class TestWorker(unittest.TestCase):
    
    # Test cases for defineGlobals
    def test_defineGlobals_valid(self):
        '''
        Test case for valid input
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        myList = [1, 2, 3]
        result = defineGlobals(myList)
        self.assertEqual(result['myList'], myList)
        self.assertEqual(result['swap'], swap)
        
    def test_defineGlobals_invalid(self):
        '''
        Test case for invalid input
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        myList = ["a", "b", "c"]
        with self.assertRaises(Exception) as context:
            defineGlobals(myList)
        self.assertEqual(str(context.exception), "All elements of the list should be integers")
        
    def test_defineGlobals_empty(self):
        '''
        Test case for empty list
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        myList = []
        with self.assertRaises(Exception) as context:
            defineGlobals(myList)
        self.assertEqual(str(context.exception), "List should not be empty")
        
    # Test cases for execute_code
    def test_execute_code_valid(self):
        '''
        Test case for valid code
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        code = "myList = [1, 2, 3]"
        initialList = [1, 2, 3]
        result = execute_code(code, [])
        self.assertEqual(result, initialList)
        
    def test_execute_code_invalid(self):
        '''
        Test case for invalid code
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        code = "myList = [1, 2, 3, 'a']"
        with self.assertRaises(Exception) as context:
            execute_code(code, [])
        self.assertEqual(str(context.exception), "All elements of the list should be integers")
        
    def test_execute_code_empty(self):
        '''
        Test case for empty code
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        code = "# Empty code"
        initialList = [1, 2, 3]
        result = execute_code(code, initialList)
        self.assertEqual(result, initialList)
        
    def test_execute_code_swap(self):
        '''
        Test case for swap function
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        code = "swap(myList, 0, 2)"
        initialList = [1, 2, 3]
        result = execute_code(code, initialList)
        self.assertEqual(result, [3, 2, 1])
        
    def test_execute_code_swap(self):
        '''
        Test case for execute_code function, using the swap function
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        code = "myList = swap(myList, 0, 1)"
        initialList = [1, 2, 3]
        result = execute_code(code, initialList)
        self.assertEqual(result, [2, 1, 3])
        
    # Test cases for swap
    def test_swap_valid(self):
        '''
        Test case for valid input in swap function
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        arr = [1, 2, 3]
        swap(arr, 0, 2)
        self.assertEqual(arr, [3, 2, 1])
        
    def test_swap_invalid(self):
        '''
        Test case for invalid input in swap function
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        arr = [1, 2, 3]
        with self.assertRaises(Exception) as context:
            swap(arr, 0, 3)
        self.assertEqual(str(context.exception), "Index out of range")
        
    def test_swap_empty(self):
        '''
        Test case for empty list in swap function
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        arr = []
        with self.assertRaises(Exception) as context:
            swap(arr, 0, 2)
        self.assertEqual(str(context.exception), "List is empty")
        
    def test_swap_empty(self):
        '''
        Test case for invalid type in swap function
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        arr = "hello world"
        with self.assertRaises(Exception) as context:
            swap(arr, 0, 3)
        self.assertEqual(str(context.exception), "Expected list, got <class 'str'>")
        
    def test_swap_valid2(self):
        '''
        Test case for valid input in swap function
        
        Parameter:
        ----------
        self : TestWorker (class)
        
        Note:
        -----
        This test case is expected to pass without raising an exception
        '''
        arr = [1, 2, 3]
        swap(arr, 0, 0)
        self.assertEqual(arr, [1, 2, 3])