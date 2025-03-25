from pyscript import document, window, PyWorker # type: ignore
import pyodide # type: ignore

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
    window.updateInExecution(True)
    
    window.incrementExecutionCount()
            
    console = window.console
    console.log("🔥 Execution Count : ", window.getExecutionCount())
    
    outputDiv = document.getElementById('output')
    assert outputDiv is not None, "Output div not found"
    
    outputDiv.innerHTML = "Creating a safe place to execute your code :)"
        
    #  Worker pour l'exécution normale
    myWorker = createWorker()
    await myWorker.ready
    assert myWorker.ready is not None, "Worker did not start properly"
    
    # Worker pour l'exécution chronométrée
    timedWorker = createWorker()
    await timedWorker.ready
    assert timedWorker.ready is not None, "Timed Worker did not start properly"
            
    myWorker.onmessage = on_worker_message
    timedWorker.onmessage = on_worker_message
    
    arr = getArr()
    code = getCode()

    console.log("💨 Worker starting execution")
    sorted_list = myWorker.sync.execute_code(code, arr, False)
    
    console.log("💨 Timed Worker starting execution")
    time = timedWorker.sync.execute_code(code, arr, True)
    
    time = await time
    
    if time is None :
        HandleError()
        terminateWorker(timedWorker, myWorker)
        return
    console.log("✅ Received result from timed Worker !")
    
    window.updateExecutionTime(time)
    
    averageTime = updateAverageTime()
    window.updateAverageTime(averageTime)
    window.updateStandardDeviation(computeStandardDeviation(averageTime))
    
    myList = await sorted_list
    
    if myList is None : 
        HandleError()
        outputDiv.innerHTML = "Something went wrong... please try again"
        terminateWorker(timedWorker, myWorker)
        return
    console.log("✅ Received results from Worker !")

    updateList(myList, len(arr) - 1, len(arr), end = True)
    
    terminateWorker(timedWorker, myWorker)
        
    window.updateInExecution(False)
    
def createWorker():
    '''
    Creates a new worker to execute the user's code
    
    Return:
    -------
    worker: The worker created to execute the user's code (PyWorker)
    '''
    worker = PyWorker("python/src/worker.py", type="pyodide")
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
    data = event.data
    outputDiv = document.getElementById('output')
    assert isinstance(data, str), f"Expected str, got {type(data)}"
    
    window.console.log("❌ Error in worker : " + event.data)

    # If the error message contains "SyntaxError" and "JSON", it means the error is related to JSON parsing.  
    # This issue arises from multiple conversions between Python and JavaScript objects.  
    # It cannot be fully corrected, only minimized (~2%).  

    if all(keyword in event.data for keyword in ["SyntaxError", "JSON"]):
        # Therefore, the user is advised to try again.  
        outputDiv.innerHTML = "Something went wrong... please try again"
    else:
        outputDiv.innerHTML = f"{event.data}"

def terminateWorker(worker1, worker2):
    '''
    Terminates the workers
    
    Parameters:
    -----------
    worker1: The worker to be terminated (PyWorker)
    worker2: The worker to be terminated (PyWorker)
    '''
    worker1.terminate()
    assert worker1.terminate, "Worker1 did not terminate properly"
    
    worker2.terminate()
    assert worker2.terminate, "Worker2 did not terminate properly"
    
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
    assert window.editor is not None, "Editor not found"
    code = window.editor.getValue()
    assert isinstance(code, str), f"Expected str, got {type(code)}"
    return code

def getArr() -> pyodide.ffi.JsProxy:
    '''
    Extracts and returns the list from the window object
    
    Return:
    -------
    arr: The list stored in the window object (pyodide.ffi.JsProxy)
    '''
    assert window.myList is not None, "List not found"
    arr = window.myList # window.myList is a pyodide.ffi.JsProxy object, can not be assert as list
    assert isinstance(arr, pyodide.ffi.JsProxy), f"Expected pyodide.ffi.JsProxy, got {type(arr)}"
    
    return arr

def getSwap():
    '''
    Gets the value of the swap variable
    
    Return:
    -------
    swap: The value of the swap variable (bool)
    '''
    return window.getSwap()

def getCompare():
    '''
    Gets the value of the compare variable
    
    Return:
    -------
    compare: The value of the compare variable (bool)
    '''
    return window.getCompare()

def getAnimationTime():
    '''
    Gets the value of the animationTime variable
    
    Return:
    -------
    animationTime: The value of the animationTime variable (int)
    '''
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
    assert isinstance(arr, pyodide.ffi.JsProxy), f"Expected pyodide.ffi.JsProxy, got {type(arr)}"
    assert isinstance(i, int), f"Expected int, got {type(i)}"
    assert isinstance(j, int), f"Expected int, got {type(j)}"
    assert isinstance(timedExecution, bool), f"Expected bool, got {type(timedExecution)}"
    assert isinstance(end, bool), f"Expected bool, got {type(end)}"
    
    if not timedExecution:
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
    executionCount = window.getExecutionCount()
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
    executionTimeList = window.getExecutionTimeList()
    variance = sum((time - averageTime) ** 2 for time in executionTimeList) / len(executionTimeList)
    standardDeviation = variance ** 0.5
    
    return standardDeviation

# Update the values of the compareCount and swapCount variables in the window object

def updateCompareCount(compareCount):
    '''
    Update the value of the compareCount variable
    '''
    window.updateCompareCount(compareCount)
    
def updateSwapCount(swapCount):
    '''
    Update the value of the swapCount variable
    '''
    window.updateSwapCount(swapCount)