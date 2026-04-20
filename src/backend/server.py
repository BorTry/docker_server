"""
Handles requests from the front end server. ensures that there is enough space for the request to be completed.
Serves the front end with information needed to run.
"""
from .lib.init import start
start()

from time import sleep
from ..lib.communication import communication
from ..lib.server_codes import Server_codes
from socket import socket, timeout
from .lib.docker_functions import *
from json import load, loads

SERVER_ADDRESS = ("0.0.0.0", 2024)
SERVER_JSON = None

# Get server information from json file
with open("./servers.json", "r") as file:
    SERVER_JSON = load(file)

server_socket = communication(SERVER_ADDRESS)

def wrap(com:communication, socket:socket):
    try:
        bdata, address = socket.recvfrom(1024)
        
        data = extract_data(bdata.decode("utf-8"))
        proc_data = process_data(data)

        if (proc_data == None):
            return

        com.send(proc_data, address)

    except timeout:
        pass

def process_data(data:dict):
    if (not docker_running):
        print("DOCKER IS NOT RUNNING")
        return Server_codes.ENGINE_NOT_RUNNING

    match data["code"]:
        case Server_codes.SERVER_COUNT:
            return get_container_count()
        case Server_codes.RUNNING_SERVERS:
            # find the resource use for each container
            all_containers = filter_container_names(get_container_names(), SERVER_JSON)
            resources_used = get_resource_use_for_containers(all_containers, SERVER_JSON)

            return resources_used
        case Server_codes.ALL_SERVERS:
            return {
                    "servers": SERVER_JSON["server_names"],
                    "launch_options": SERVER_JSON["launch_alternatives"]
                }

        case Server_codes.START_SERVER:
            start_server(data["data"], SERVER_JSON)

        case Server_codes.GET_USAGE:
            get_container_ramusage(data["data"], SERVER_JSON)

def extract_data(response:str):
    return loads(response)

def main():
    server_socket.start(wrap)

    while True:
        try:
            user_in = input("Select Action: ")

            if (user_in == "quit" or user_in == "q"):
                return

            sleep(1)
            
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
    print("Cleaning shit up")
    stop_frontend()
    server_socket.stop()