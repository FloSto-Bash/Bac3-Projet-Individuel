from pyscript import document, window, PyWorker     # type: ignore
import pyodide                                      # type: ignore

async def startWorker(event):
    '''
    Creates a new worker to execute the user's code and returns the result
    
    Parameter:
    -----------
    event: Event
    
    Note:
    ------
    This function is called when the user clicks the "Execute code" button
    '''
    assert window is not None, "Window not found, in startWorker"
    window.updateInExecution(True)
    
    window.incrementExecutionCount()
            
    console = window.console
    assert console is not None, "Console not found, in startWorker"
    console.log("🔥 Execution Count : ", window.getExecutionCount())
    
    outputDiv = document.getElementById('output')
    assert outputDiv is not None, "Output div not found, in startWorker"
    
    outputDiv.innerHTML = "Creating a safe place to execute your code :)"
        
    #  Worker for the "normal" execution
    myWorker = createWorker()
    await myWorker.ready
    assert myWorker.ready is not None, "Worker did not start properly, in startWorker"
    
    # Worker for the "measuring" execution
    # This worker is used to measure the time taken for the execution of the user's code
    timedWorker = createWorker()
    await timedWorker.ready
    assert timedWorker.ready is not None, "Timed Worker did not start properly, in startWorker"
    
    # Set the onmessage function for both workers
    # This function allows to handle the messages sent by the worker
    myWorker.onmessage = on_worker_message
    timedWorker.onmessage = on_worker_message
    
    arr = getArr()
    assert arr is not None, "Array not found, in startWorker"
    assert isinstance(arr, pyodide.ffi.JsProxy), f"Expected pyodide.ffi.JsProxy, got {type(arr)}, in startWorker"
    assert len(arr) > 0, "Array is empty, in startWorker"
    
    code = getCode()
    assert code is not None, "Code not found, in startWorker"
    assert isinstance(code, str), f"Expected str, got {type(code)}, in startWorker"

    console.log("💨 Worker starting execution")
    sorted_list = myWorker.sync.execute_code(code, arr, False)
    
    console.log("💨 Timed Worker starting execution")
    time = timedWorker.sync.execute_code(code, arr, True)
    
    time = await time
    
    # Handle unexpected errors (mostly related to JSON parsing)
    if time is None :
        HandleError()
        terminateWorkers(timedWorker, myWorker)
        return
    console.log("✅ Received result from timed Worker !")
    
    window.updateExecutionTime(time)
    
    averageTime = updateAverageTime()
    assert averageTime is not None, "Average time not found, in startWorker"

    window.updateAverageTime(averageTime)
    window.updateStandardDeviation(computeStandardDeviation(averageTime))
    
    myList = await sorted_list
    
    # Handle unexpected errors (mostly related to JSON parsing)
    if myList is None : 
        HandleError()
        outputDiv.innerHTML = "Something went wrong... please try again"
        terminateWorkers(timedWorker, myWorker)
        return
    console.log("✅ Received result from Worker !")

    # Update the final two elements of the list
    updateList(myList, len(arr) - 1, len(arr), end = True)
    
    terminateWorkers(timedWorker, myWorker)
        
    window.updateInExecution(False)
    
def createWorker():
    '''
    Creates a new worker to execute the user's code
    
    Return:
    -------
    worker: The worker created to execute the user's code (PyWorker)
    
    Note:
    ------
    This function creates a new worker to execute the user's code. The worker is created using the PyWorker class.
    The worker is created with the file "python/src/worker.py". The worker is used to execute the user's code in a separate thread.
    Various functions have been added to the worker, to allow interaction between the user's code and the frontend.
    '''
    worker = PyWorker("python/src/worker.py", type="pyodide")
    assert worker is not None, "Worker not found, in createWorker"
    worker.sync.compareOnDiagram = compareOnDiagram
    worker.sync.updateList = updateList
    worker.sync.getSwap = getSwap
    worker.sync.getCompare = getCompare
    worker.sync.getAnimationTime = getAnimationTime
    worker.sync.updateCompareCount = updateCompareCount
    worker.sync.updateSwapCount = updateSwapCount
    return worker

def on_worker_message(event):
    '''
    Handles the messages sent by the worker
    
    Parameters:
    -----------
    event: Event
    
    Note:
    ------
    This function is called when the worker sends a message. The worker only sends messages when an error occurs.
    When a message is received, the function displays the error message in the output div and log the error in the console.
    
    event.data : The error message sent by the worker (str)
    '''
    assert window is not None, "Window not found, in on_worker_message"
    assert event is not None, "Event not found, in on_worker_message"
    
    data = event.data
    assert data is not None, "Data not found, in on_worker_message"
    assert isinstance(data, str), f"Expected str, got {type(data)}, in on_worker_message"
    
    outputDiv = document.getElementById('output')
    assert outputDiv is not None, "Output div not found, in on_worker_message"
    
    window.console.log("❌ Error in worker : " + event.data)

    # If the error message contains "SyntaxError" and "JSON", it means the error is related to JSON parsing.  
    # This issue arises from multiple conversions between Python and JavaScript objects.  
    # It cannot be fully corrected, only minimized (between 2 and 5 %).  

    if all(keyword in event.data for keyword in ["SyntaxError", "JSON"]):
        # Therefore, the user is advised to try again.  
        outputDiv.innerHTML = "Something went wrong... please try again"
    else:
        outputDiv.innerHTML = event.data

def terminateWorkers(worker1, worker2):
    '''
    Terminates the two workers
    
    Parameters:
    -----------
    worker1: The worker to be terminated (PyWorker)
    worker2: The worker to be terminated (PyWorker)
    '''
    worker1.terminate()
    assert worker1.terminate, "Worker1 did not terminate properly, in terminateWorkers"
    
    worker2.terminate()
    assert worker2.terminate, "Worker2 did not terminate properly, in terminateWorkers"
    
def HandleError():
    '''
    Handles the case when an error occurs during the execution of the user's code
    '''
    window.decrementExecutionCount()
    window.updateInExecution(False)
    
    window.stopComparing()
    window.resetGrid()

# Get functions to extract the values from the window object

def getCode() -> str:
    '''
    Extracts and returns the code from the editor

    Return:
    -------
    code: The code entered by the user in the editor (str)
    '''
    assert window.editor is not None, "Editor not found, in getCode"
    code = window.editor.getValue()
    assert isinstance(code, str), f"Expected str, got {type(code)}, in getCode"
    return code

def getArr() -> pyodide.ffi.JsProxy:
    '''
    Extracts and returns the list from the window object
    
    Return:
    -------
    arr: The list stored in the window object (pyodide.ffi.JsProxy)
    '''
    assert window.myList is not None, "List not found, in getArr"
    arr = window.myList 
    # window.myList is a pyodide.ffi.JsProxy object, can not be assert as list
    assert isinstance(arr, pyodide.ffi.JsProxy), f"Expected pyodide.ffi.JsProxy, got {type(arr)}, in getArr"
    
    return arr

def getSwap():
    '''
    Gets the value of the swap variable
    
    Return:
    -------
    swap: The value of the swap variable (bool)
    '''
    assert window is not None, "Window not found, in getSwap"
    return window.getSwap()

def getCompare():
    '''
    Gets the value of the compare variable
    
    Return:
    -------
    compare: The value of the compare variable (bool)
    '''
    assert window is not None, "Window not found, in getCompare"
    return window.getCompare()

def getAnimationTime():
    '''
    Gets the value of the animationTime variable
    
    Return:
    -------
    animationTime: The value of the animationTime variable (int)
    '''
    assert window is not None, "Window not found, in getAnimationTime"
    return window.getAnimationTime()

# Functions that update the animation of the diagram

def compareOnDiagram(i : int, j : int):
    '''
    Compares two elements on the diagram
    
    Parameters:
    -----------
    i : The index of the first element (int)
    j : The index of the second element (int)
    '''
    assert window is not None, "Window not found, in compareOnDiagram"
    window.compareOnDiagram(i, j)

def updateList(arr, i, j, timedExecution = False, end = False) :
    '''
    Updates the list displayed in the window
    
    Parameters:
    -----------
    arr: The list to be displayed (pyodide.ffi.JsProxy)
    i : The index of the first element (int)
    j : The index of the second element (int)
    timedExecution : Boolean to indicate if the execution is timed (bool) (default = False)
    end : Boolean to indicate the end of the sorting process (bool) (default = False)
    '''
    assert isinstance(arr, pyodide.ffi.JsProxy), f"Expected pyodide.ffi.JsProxy, got {type(arr)}, in updateList"
    assert isinstance(i, int) and not isinstance(i, bool), f"Expected int, got {type(i)}, in updateList"
    assert isinstance(j, int) and not isinstance(i, bool), f"Expected int, got {type(j)}, in updateList"
    assert isinstance(timedExecution, bool), f"Expected bool, got {type(timedExecution)}, in updateList"
    assert isinstance(end, bool), f"Expected bool, got {type(end)}, in updateList"
    
    if not timedExecution:
        assert window is not None, "Window not found, in updateList"
        window.updateList(arr)
        if getSwap() and not end:
            window.swapOnDiagram(i, j)
        if end : 
            window.stopComparing()

# Compute the average time and standard deviation
   
def updateAverageTime() -> float:
    '''
    Updates the average time taken for execution

    Returns:
    --------
    newAverage: The updated average time taken for execution (float)
    '''
    assert window is not None, "Window not found, in updateAverageTime"

    executionCount = window.getExecutionCount()
    assert executionCount > 0, "Execution count value is negative, in updateAverageTime"
    executionTimeList = window.getExecutionTimeList()
    
    return sum(executionTimeList) / executionCount

def computeStandardDeviation(averageTime) -> float:
    '''
    Computes the standard deviation of the time taken for execution
    
    Parameters:
    -----------
    averageTime: The average time taken for execution (float)
    
    Return:
    -------
    standardDeviation: The standard deviation of the time taken for execution (float)
    '''
    assert window is not None, "Window not found, in computeStandardDeviation"
    
    executionTimeList = window.getExecutionTimeList()
    assert len(executionTimeList) > 0, "Length of executionTimeList is negative, in computeStandardDeviation"
    
    variance = sum((time - averageTime) ** 2 for time in executionTimeList) / len(executionTimeList)
    standardDeviation = variance ** 0.5
    
    return standardDeviation

# Update the values of the compareCount and swapCount variables in the window object

def updateCompareCount(compareCount):
    '''
    Update the value of the compareCount variable
    '''
    assert window is not None, "Window not found, in updateCompareCount"
    
    window.updateCompareCount(compareCount)
    
def updateSwapCount(swapCount):
    '''
    Update the value of the swapCount variable
    '''
    assert window is not None, "Window not found, in updateSwapCount"
    
    window.updateSwapCount(swapCount)