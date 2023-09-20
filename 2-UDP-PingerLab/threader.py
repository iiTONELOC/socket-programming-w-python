import threading
import ctypes

class ThreadManager:
    '''
        This class manages a thread so that it can be stopped gracefully or
        forcefully
        
        args:
            target: the function to run in the thread
            args: the arguments to pass to the target function
            name: the name of the thread
    '''
    def __init__(self, target=None, args=(), name=None):
        self.target = target
        self.args = args
        self.name = name
        self.thread = None

    def _thread_function_wrapper(self):
        '''
            Creates a wrapper function for the target function so that any
            exceptions raised by the target function can be caught
        '''
        try:
            self.target(*self.args)
        except Exception as e:
            print(f"Thread {self.name} raised an exception: {e}")

    def start(self):
        '''
            Starts the thread and runs the target function
        '''
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._thread_function_wrapper, name=self.name)
            self.thread.daemon = True
            self.thread.start()

    def stop(self, timeout=5):
        '''
            Stops the thread gracefully or forcefully if it doesn't stop within
            the timeout. A default timeout of 5 seconds is used but this can be
            overridden by passing a different value to the timeout parameter
        '''
        if self.thread is not None and self.thread.is_alive():
            # Attempt a graceful stop first
            self.thread.join(timeout)
            
            # If it doesn't stop within the timeout, escalate to forceful termination
            if self.thread.is_alive():
                self.terminate_thread(self.thread)
                self.thread = None

    @staticmethod
    def terminate_thread(thread: threading.Thread)->None:
        '''
            Terminates a thread forcefully
            
            args:
                thread: the thread object to terminate
            
            returns: None
        '''
        if not thread.is_alive():
            return
        # The thread is still alive so we need to terminate it forcefully
        # We do this by raising an exception in the thread and catching it
        thread_id = ctypes.c_long(thread.ident)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))

        
        if res == 0:
            raise ValueError("Nonexistent thread ID")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")
