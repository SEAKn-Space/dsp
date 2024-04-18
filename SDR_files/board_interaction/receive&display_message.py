#!/usr/bin/python3
# -*- coding: utf-8 -*-

# zmq_SUB_proc.py
# Author: Marc Lichtman

import zmq
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import base64
from PIL import Image

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:100100") # connect, not bind, the PUB will bind, only 1 can bind
socket.setsockopt(zmq.SUBSCRIBE, b'') # subscribe to topic of all (needed or else it won't work)

prev_data = np.zeros(128)

f_out = open ('received_image.png', 'wb')
Pkt_len = 52
state = 0
buffer = ""
_debug = 0

while True:
    if socket.poll(10) != 0 or state==1: # check if there is a message on the socket
        msg = socket.recv() # grab the message
        print(len(msg)) # size of msg
        data = np.frombuffer(msg, dtype=np.byte, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
        print(data)

        buffer += str(data)

        if len(buffer) < Pkt_len and state == 0:
            continue

        if (state == 0):
            # grab next packet from buffer
            buff =  buffer[:Pkt_len]
            buffer = buffer[Pkt_len:]
            b_len = len(buff)

            if ((buff[0] == 37) and (buff[51] == 93)):
                continue
            else:
                # decode Base64
                collected_data = base64.b64decode(buff + str(b'=='))
                f_out.write (collected_data)
                if (_debug):
                    print ("End of preamble")
                state = 1
                continue

        elif (state == 1):
            # grab next packet from buffer
            buff =  buffer[:4]
            buffer = buffer[4:]
            b_len = len(buff)

            if b_len == 0:
                print ('End of file')
                break
            if (buff[0] == 37):     # '%'
                if (buff == b'%UUU'):
                    print ("End of text")
                    buff =  buffer[:4] # skip next four 'U's
                    buffer = buffer[4:]
                    
                    rcv_fn = []
                    i = 0
                    while (i < 44):
                        ch = buffer[0]
                        buffer = buffer[0]
                        if (ch == b'%'):
                            break
                        rcv_fn.append((ord)(ch))
                        i += 1
                    rf_len = len (rcv_fn)
                    x = 0
                    while (x < rf_len):
                        rcv_fn[x] = str((chr)(rcv_fn[x]))
                        x += 1
                    ofn = "".join(rcv_fn)
                    print ("Transmitted file name:",ofn)
                    
                    state = 2
                    continue
            else:
                # decode Base64
                collected_data = base64.b64decode(buff+str(b'=='))
                f_out.write (collected_data)
                print("maybe ???")

                continue

    elif (state == 2):
        # Open the image file
        try:
            f_out.close()
            img = Image.open('received_image.png')
            img.show()
        except:
            print('Error: Could not open image file')

        # Prepare for next received file/image
        # state = 0
        exit(0)
        continue

    else:
        time.sleep(0.1) # wait 100ms and try again