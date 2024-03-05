import os
import time
import sys
import cv2

#grab systems args
fn = sys.argv[1]
out = sys.argv[2]
prev_time = os.path.getmtime(fn)# get the last modifed time of the file

#Loop that keeps track of the file
while True:
    t = os.path.getmtime(fn) #Check the modifed time of the file
    if t != prev_time: #if its different
        prev_time = t
        t_start=time.time()
        while time.time() < t_start+1: # A loop that waits until the 2 seconds have passed from last file update
            t=os.path.getmtime(fn)
            if t != prev_time:
                t_start = time.time()
                prev_time=t
        os.system("python3 .\strip_preamble.py {} {}".format(fn,out))#stip the preamble
        print("Thing Happend ;)")
        prev_time = t
