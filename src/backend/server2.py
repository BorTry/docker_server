from threading import Lock, Event
from multiprocessing import Pipe

from src.lib.ez_thread import ez_thread
from src.backend.lib.comm_thread import comm_func
from src.backend.lib.docker_thread import docker_func
from src.lib.server_codes import Server_codes

from runpy import run_path
run_path("./src/backend/lib/init.py") # Init file

thread_lock = Lock()
thread_pipe = Pipe(duplex=True)
thread_terminate_event = Event()

COMMMUNICATION_THREAD = ez_thread(
    target=comm_func,
    terminate_signal=thread_terminate_event,
    name="comm_thread",
    pipe=thread_pipe,
    lock=thread_lock
) # Talks to the frontend server

DOCKER_THREAD = ez_thread(
    target=docker_func,
    terminate_signal=thread_terminate_event,
    name="docker_thread",
    pipe=thread_pipe,
    lock=thread_lock
) # Talks to the docker engine


def main():
    pass

if __name__ == "__main__":
    main()