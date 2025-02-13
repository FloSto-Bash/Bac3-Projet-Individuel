export const initialCode = 
`"""
To execute your code, use the 'play' button on the right side of the screen, just like if you were running a normal Python code.
You must use the predefined functions 'swap' and 'compare' in your code, otherwise the animation will not work.

The selected list in the animation is called 'myList', and it is the list that you should sort.
You can not redefine 'myList' in your code.

Here is the description of the predefined functions:

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
    '''

def swap(arr : list, i : int, j : int):
    '''
    Swaps the elements at the given indices in the list
    
    Parameters:
    -----------
    arr: The list in which the elements are to be swapped (list)
    i: The index of the first element (int)
    j: The index of the second element (int)
    '''

You can try this code to see the effect of the predefined functions
"""
# Be sure to activate the check box 'Show compare' to see the output of the code
compare(myList, 0, 1)

# Be sure to activate the check box 'Show swap' to see the output of the code
swap(myList, 0, 1)
`;