import ctypes
import threading

from setting.log_handler import logger

thread_list = []


class ThreadWithException(threading.Thread):    
    def get_id(self): 
        '''
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        '''
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def terminate(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 


def close_thread(func):
    global thread_list

    logger.debug("[DEBUG] func %s start close threads : %s" %(func, thread_list))

    for thread in thread_list:
        thread.terminate()

    thread_list = []
    logger.debug("[DEBUG] func %s finish close threads" %func)