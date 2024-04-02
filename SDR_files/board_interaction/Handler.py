import os
import subprocess
import numpy as np

def main(queue):
    print("I AM THE HANDLER")
    
    # Board communication here
    # BPSK = 0
    # QPSK = 1
    while True:
        data = queue.get()
        data = data.flatten()
        print("Got Data")
        # print(type(data))
        # print(len(data))
        # print(data)


    # print("Goodbye World!")
    