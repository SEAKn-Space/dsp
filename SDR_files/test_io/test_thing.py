import numpy as np
from scipy import fft
import sys
import subprocess
import multiprocessing as mp
import time

def f():
    start = time.time()
    with open("test.txt",'w') as sys.stdout:
        while 1 >= time.time()-start:
            print("test")
        print("exit")
    return


if __name__ == '__main__':
    p = mp.Process(target=f)
    p.start()
    thing = open("testy.txt",'r')
    for line in thing:
        if 'exit' == line.strip():
                print('Found exit. Terminating the program')
                break
    p.join()
   





