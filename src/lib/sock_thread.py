from src.lib.ez_thread import ez_thread
from socket import socket, AF_INET, SOCK_DGRAM
from json import load, dumps, loads
from os import path

from typing import Callable, Any
from threading import Event

BUFFER_SIZE = 1024
CONNECTION_TYPE = [AF_INET, SOCK_DGRAM]
SOCK_PATH = None # Used only on Linux

CONFIG_FILE_PATH = path.abspath("./resources/config.json")
CONFIG_JSON = None

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG_JSON = load(file)

if (CONFIG_JSON["os"] == "Linux"):
    from socket import AF_UNIX
    CONNECTION_TYPE[0] = AF_UNIX
    SOCK_PATH = "./resources/sock"

class sock_thread(ez_thread):
    def __init__(self, target:Callable=None, init:Callable=None, address:tuple[str, int]=None, target_address:tuple[str, int]=None, terminate_signal:Event=None, name:str="thread", sleeptime:float=0.0):
        if (not address):
            raise Exception("Socket thread needs an address to bind to")

        self.target_address = target_address # Only given if a socket thread needs to send and wait for an answer

        self.socket = socket(*CONNECTION_TYPE)
        self.socket.bind(SOCK_PATH or address)

        self.socket.settimeout(0.25)

        super().__init__(target, init, terminate_signal, name, None, sleeptime)

    def send(self, data:str, code:int=200, target:tuple[str, int]=None):
        target_address = target or self.target_address

        if (not target_address):
            raise ValueError("Target address not defined, in class or function")
        
        data_packet = {
            "code": code,
            "data": data
        }

        self.socket.sendto(encode(data_packet), target_address)

    def recv(self):
        try:
            new_data, address = self.socket.recvfrom(BUFFER_SIZE)

            return decode(new_data), address
        except:
            return None, None

    def send_recv(self, code:int, data:str=""):
        self.send(data=data, code=code)
        new_data, _ = self.recv()

        return new_data

def encode(data:Any):
    return dumps(data).encode("utf-8")

def decode(data:bytes):
    return loads(data.decode("utf-8"))