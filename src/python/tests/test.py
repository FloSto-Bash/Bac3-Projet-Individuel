# File to test the error message from different functions, to catch the error message and compare using self.assertEqual in the test cases.

def compare(arr, a, b):
    return arr[a] <= arr[b]

def swap(arr, i, j):
    assert arr != [], "List should not be empty"
    assert i < len(arr), "Index out of range"
    assert j < len(arr), "Index out of range"
    assert isinstance(arr, list), f"Expected list, got {type(arr)}"
    
    arr[i], arr[j] = arr[j], arr[i]
    
arr = "hello"
swap(arr, 0, 0)
print(arr)