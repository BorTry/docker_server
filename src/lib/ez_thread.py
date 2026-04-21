from threading import Thread, Event
from sys import stdout
from time import sleep

# Typing for very nice :)  
from typing import Callable, Any
from multiprocessing.connection import Connection
from _thread import LockType

class ez_thread:
    def __init__(self, target:Callable=None, terminate_signal:Event=None, name="thread", pipe:Connection=None, lock:LockType=None, sleep_time:float=0.1):
        self.name = name
        self.stdout = stdout
        self.sleep_time = sleep_time

        if not target:
            raise Exception("target function must be defined")
        
        self.thread = Thread(target=thread_wrapper(self, target), name=name)
        self.terminate_signal = terminate_signal or Event()

        if ((pipe and not lock) or (not pipe and lock)):
            raise Exception("Pipe and lock must both be defined")
        
        self.pipe = pipe
        self.lock = lock

    def print(self, *msg:tuple[str]):
        print(self.name, *msg, file=stdout)

    def read_value(self):
        val = None

        with self.lock:
            val = self.pipe.recv()

        return val
    
    def send_value(self, val:Any):
        with self.lock:
            self.pipe.send(val)

    def data_in_pipe(self):

        return self.pipe.poll()

    def terminate(self):
        # Check if the pipe is still open
        try:
            self.pipe.send("hello")
            self.pipe.close()
        except BrokenPipeError:
            pass

        # Close the thread and wait for it to finish
        if (not self.terminate_signal.is_set()):
            self.terminate_signal.set() # Multiple threads can use the same event signal

        if self.thread and self.thread.is_alive():
            print(f"Waiting for {self.thread.name} to terminate")
            self.thread.join()

    def run(self):
        self.thread.start()

def thread_wrapper(self:ez_thread, target:Callable):
    def wrap():
        while not self.terminate_signal.is_set():
            target(self)

            sleep(self.sleep_time)

    return wrap