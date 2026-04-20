"""
Used for a connection between the front end server, and the back end
"""

from threading import Thread, Event
from sys import stdout
from typing import Callable
from json import dumps, load
from os import path

CONFIG_FILE_PATH = path.abspath("./resources/config.json")
CONFIG_JSON = None

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG_JSON = load(file)

if (not CONFIG_JSON):
    raise Exception("Something went wrong while opening config file")

if (CONFIG_JSON["os"] == "Linux"):
    from socket import socket, AF_UNIX, SOCK_DGRAM
else:
    from socket import socket, AF_INET, SOCK_DGRAM

class communication:
    def __init__(self, address:tuple[str, int], name:str="com", target_address:tuple[str, int]=None, is_server=False):
        if (not address):
            raise ValueError("Address not defined")
        
        self.stdout = stdout

        if (CONFIG_JSON["os"] == "Linux"):
            self.socket = socket(AF_UNIX, SOCK_DGRAM)
            self.socket.bind("./resources/sock")
            print("./resources/sock")
        else:
            self.socket = socket(AF_INET, SOCK_DGRAM)
            self.socket.bind(address)
            print(address)

        
        self.thread = None
        self.terminate = Event()

        self.thread_val = None

        self.name = name
        self.target_addr = target_address

    def print(self, *msg:str) -> None:
        print(*msg, file=self.stdout)

    def start(self, wrap:Callable):
        """
        Start a thread with the wrapper attached.
        The wrapper function is passed to another wrapper that handles looping and terminating. 
        The wrap function is passed this class, and the socket.
        The return value from the wrap function is set to th 'thread_val' variable in this class
        """

        if (self.thread):
            print("Tried to start new thread, but one already exists..")
            return

        self.socket.settimeout(0.25)

        def outer_wrap():
            while not self.terminate.is_set():
                self.thread_val = wrap(self, self.socket)

        self.thread = Thread(target=outer_wrap, name=self.name)
        self.thread.start()

    def send(self, data:str, target:tuple[str, int]=None, code:int=200):
        if (not target and not self.target_addr):
             raise ValueError("Target address not defined")
        
        data_packet = {
            "code": code,
            "data": data
        }

        self.socket.sendto(dumps(data_packet).encode("utf-8"), self.target_addr if not target else target)

    def send_recv(self, code:int, data:str=""):
        if (not self.target_addr):
             raise ValueError("Target address not defined")
        
        data_packet = {
            "code": code,
            "data": data
        }

        self.socket.sendto(dumps(data_packet).encode("utf-8"), self.target_addr)

        new_data, _ = self.socket.recvfrom(1024)

        return new_data.decode()

    def stop(self):
        self.terminate.set()

        if self.thread and self.thread.is_alive():
            print(f"Waiting for {self.thread.name} to terminate")
            self.thread.join()