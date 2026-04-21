"""
Run function for the comm thread
"""
from src.lib.ez_thread import ez_thread

# holds anto a dict that gets updated by the docker thread
# when a request from the frontend server comes in send the requested data from that dict over

def comm_func(ez_thread:ez_thread):
    pass