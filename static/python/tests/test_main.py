import unittest
from unittest.mock import MagicMock

from ..src.main import getArr, getCode, compare, updateList

# Mock solution provided by GitHub Copilot

class TestMain(unittest.TestCase):

    def test_getArr_valid(self, mock_window):
        '''
        Test the getArr function with a valid list
        
        Parameters:
        -----------
        self : TestMain (class)
        mock_window : MagicMock (class)
        '''
        mock_window.myList = [1, 2, 3]
        result = getArr()
        self.assertEqual(result, [1, 2, 3])
        
    def test_getArr_none(self, mock_window):
        '''
        Test the getArr function with a None list
        
        Parameters:
        -----------
        self : TestMain (class)
        mock_window : MagicMock (class)
        '''
        # Mock window.myList to be None
        mock_window.myList = None
        with self.assertRaises(AssertionError) as context:
            getArr()
        self.assertEqual(str(context.exception), "List not found")

    # Test cases for getCode
    def test_getCode_valid(self, mock_window):
        '''
        Test the getCode function with a valid code
        
        Parameters:
        -----------
        self : TestMain (class)
        mock_window : MagicMock (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        mock_window.editor.getValue.return_value = "myList = [1, 2, 3]"
        result = getCode()
        self.assertEqual(result, "myList = [1, 2, 3]")
        
    def test_getCode_none(self, mock_window):
        '''
        Test the getCode function with a None code
        
        Parameters:
        -----------
        self : TestMain (class)
        mock_window : MagicMock (class)
        
        Note:
        -----
        This test case is expected to raise an exception
        '''
        # Mock window.editor.getValue to be None
        mock_window.editor.getValue.return_value = None
        with self.assertRaises(AssertionError) as context:
            getCode()
        self.assertEqual(str(context.exception), "Expected str, got <class 'NoneType'>")
    
    # Test cases for compare
    def test_compare_true(self):
        '''
        Test the compare function with arr[i] <= arr[j]
        
        Parameter:
        ----------
        self : TestMain (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        result = compare([1, 2], 0, 1)
        self.assertEqual(result, True)
        
    def test_compare_false(self):
        '''
        Test the compare function with arr[i] > arr[j]
        
        Parameter:
        ----------
        self : TestMain (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        result = compare([2, 1], 0, 1)
        self.assertEqual(result, False)
        
    def test_compare_equal(self):
        '''
        Test the compare function with arr[i] == arr[j]
        
        Parameter:
        ----------
        self : TestMain (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        result = compare([1, 1], 0, 1)
        self.assertEqual(result, True)
        
    # Test cases for updateList
    def test_updateList_valid(self, mock_window):
        '''
        Test the updateList function with valid parameters
        
        Parameter:
        ----------
        self : TestMain (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        mock_window.myList = [1, 2, 3]
        mock_window.swap = False
        arr = [1, 2, 3]
    
        mock_window.updateList = MagicMock()
        mock_window.swapOnDiagram = MagicMock()
        mock_window.stopComparing = MagicMock()
        
        updateList(arr, 0, 2)
        
        self.assertEqual(arr, [1, 2, 3])
        
        mock_window.updateList.assert_called_with(arr)
        
        mock_window.swapOnDiagram.assert_not_called()
        mock_window.stopComparing.assert_not_called()
        
    def test_updateList_swap(self, mock_window):
        '''
        Test the updateList function with swap = True
        
        Parameter:
        ----------
        self : TestMain (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        mock_window.myList = [1, 2, 3]
        mock_window.swap = True
        arr = [1, 2, 3]
        
        mock_window.updateList = MagicMock()
        mock_window.swapOnDiagram = MagicMock()
        mock_window.stopComparing = MagicMock()
        
        updateList(arr, 0, 2)
        
        self.assertEqual(arr, [3, 2, 1])
        
        mock_window.updateList.assert_called_with(arr)
        mock_window.swapOnDiagram.assert_called_with(0, 2)
        
        mock_window.stopComparing.assert_not_called()
        
    def test_updateList_end(self, mock_window):
        '''
        Test the updateList function with end = True
        
        Parameter:
        ----------
        self : TestMain (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        mock_window.myList = [1, 2, 3]
        mock_window.swap = False
        arr = [1, 2, 3]
        
        mock_window.updateList = MagicMock()
        mock_window.swapOnDiagram = MagicMock()
        mock_window.stopComparing = MagicMock()
        
        updateList(arr, 0, 2, end=True)
        
        self.assertEqual(arr, [1, 2, 3])
        
        mock_window.updateList.assert_called_with(arr)
        mock_window.stopComparing.assert_called()
        
        mock_window.swapOnDiagram.assert_not_called()
        
    def test_updateList_swap_end(self, mock_window):
        '''
        Test the updateList function with swap = True and end = True
        
        Parameter:
        ----------
        self : TestMain (class)
        
        Note:
        -----
        This test case is expected to pass
        '''
        mock_window.myList = [1, 2, 3]
        mock_window.swap = True
        arr = [1, 2, 3]
        
        mock_window.updateList = MagicMock()
        mock_window.swapOnDiagram = MagicMock()
        mock_window.stopComparing = MagicMock()
        
        updateList(arr, 0, 2, end=True)
        
        self.assertEqual(arr, [3, 2, 1])
        
        mock_window.updateList.assert_called_with(arr)
        mock_window.swapOnDiagram.assert_called_with(0, 2)
        mock_window.stopComparing.assert_called()
        
if __name__ == '__main__':
    unittest.main()