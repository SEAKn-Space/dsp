import os
import time
import sys

fn = "./out_File"
prev_time = os.path.getmtime(fn)

while True:
    t = os.path.getmtime(fn)
    if t != prev_time:
        prev_time = t
        t_start=time.time()
        while time.time() < t_start+2:
            t=os.path.getmtime(fn)
            if t != prev_time:
                t_start = time.time()
                prev_time=t
        os.system("python3 ./strip_preamble.py {} ./output.png".format(fn))
        # seperated = fn.split(".")
        print("Thing Happend ;)")
        prev_time = t