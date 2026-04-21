# initializes extra resources for the server

from json import load, dumps
import docker
from platform import system
import os
from src.backend.lib.docker_functions import docker_running

CLIENT = docker.from_env()
CONFIG_FILE_PATH = os.path.abspath("./resources/config.json")
SERVER_JSON_FILE_PATH = "./servers.json"

# initialize the reverse container name to server name
def initialize_servers_json():
    json_servers = {}
    with open(SERVER_JSON_FILE_PATH, "r") as file:
        json_servers = load(file)

    container_names_json = json_servers["container_to_server_names"]
    json_servers["server_names_to_container"] = {}

    for container_name, server_name in container_names_json.items():
        json_servers["server_names_to_container"][server_name] = container_name

    with open(SERVER_JSON_FILE_PATH, "w") as file:
        file.write(dumps(json_servers, indent=4))

def fill_config():
    json_obj = None

    with open(CONFIG_FILE_PATH, "r") as file:
        json_obj = load(file)

    if (not json_obj):
        raise Exception("Something went wrong while opening config file")

    json_obj["os"] = system()

    with open(CONFIG_FILE_PATH, "w") as file:
        file.write(dumps(json_obj, indent=4))

def start_frontend(): 
    # check to see if the docker container exists at all
    if (not len(CLIENT.containers.list(filters={"name": "docker_server-frontend-1"}, all=True))):
        raise Exception("Front end container does not exist")
    
    frontend = CLIENT.containers.get("docker_server-frontend-1")
    frontend.start()

def start():
    if (not docker_running()):
        raise Exception("Docker engine is not running")
    
    initialize_servers_json()
    fill_config()
    #start_frontend()

start()