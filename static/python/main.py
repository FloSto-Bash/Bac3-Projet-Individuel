from pyscript import document, window, PyWorker # type: ignore
import pyodide # type: ignore

def on_worker_message(event):
    data = event.data
    outputDiv = document.getElementById('output')
    if isinstance(data, str) : 
        window.console.log("❌ Error in worker : " + event.data)
        keywords = ["SyntaxError", "JSON"]
        if all(keyword in event.data for keyword in keywords):
            outputDiv.innerHTML = "Something went wrong... please try again"
        else:
            outputDiv.innerHTML = f"{event.data}"

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
        endingWithError()
        terminateWorker(timedWorker, myWorker)
        return
    console.log("✅ Received result from timed Worker !")
    
    window.updateExecutionTime(time)
    
    averageTime = updateAverageTime()
    window.updateAverageTime(averageTime)
    window.updateStandardDeviation(computeStandardDeviation(averageTime))
    
    myList = await sorted_list
    
    if myList is None : 
        endingWithError()
        outputDiv.innerHTML = "Something went wrong... please try again"
        terminateWorker(timedWorker, myWorker)
        return
    console.log("✅ Received results from Worker !")

    updateList(myList, len(arr) - 1, len(arr), end = True)
    
    terminateWorker(timedWorker, myWorker)
        
    window.updateInExecution(False)
    
def createWorker():
    worker = PyWorker("python/worker.py", type="pyodide")
    worker.sync.compareOnDiagram = compareOnDiagram
    worker.sync.updateList = updateList
    worker.sync.getSwap = getSwap
    worker.sync.getCompare = getCompare
    worker.sync.getAnimationTime = getAnimationTime
    worker.sync.updateCompareCount = updateCompareCount
    worker.sync.updateSwapCount = updateSwapCount
    return worker

def terminateWorker(worker1, worker2):
    worker1.terminate()
    assert worker1.terminate, "Worker1 did not terminate properly"
    
    worker2.terminate()
    assert worker2.terminate, "Worker2 did not terminate properly"
    
def endingWithError():
    window.decrementExecutionCount()
    window.updateInExecution(False)
    
    window.stopComparing()
    window.resetGrid()

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
    arr: The list to be displayed (pyodide.ffi.object)
    i : The index of the first element (int)
    j : The index of the second element (int)
    timedExecution : Boolean to indicate if the execution is timed (bool) (default = False)
    end : Boolean to indicate the end of the sorting process (bool) (default = False)
    '''
    if not isinstance(arr, pyodide.ffi.JsProxy) :
        arr = pyodide.ffi.to_js(arr)
    
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

def getSwap():
    return window.getSwap()

def getCompare():
    return window.getCompare()

def getAnimationTime():
    return window.getAnimationTime()

def updateCompareCount(compareCount):
    window.updateCompareCount(compareCount)
    
def updateSwapCount(swapCount):
    window.updateSwapCount(swapCount)