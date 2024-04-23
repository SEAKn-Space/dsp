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

file_path = 'received_image.png'
# f_out = open (file_path, 'wb')
Pkt_len = 52
state = 0
buffer = ""
_debug = 1

working = True
while True:
    print("Ready for next file!")
    with open(file_path, 'wb') as f_out:
        while working:
            # print("in loop")
            if socket.poll(10) != 0: # check if there is a message on the socket
                msg = socket.recv() # grab the message
                # print(len(msg)) # size of msg
                data = np.frombuffer(msg, dtype=np.byte, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
                # print(data)

                data_str = [chr(i) for i in data]
                data_str = ''.join(data_str)

                buffer += data_str
                # print("buffer len:",len(buffer))

            elif len(buffer) > 0:
                # if len(buffer) < Pkt_len:
                #     continue

                if (state == 0):
                    # grab next packet from buffer
                    buff =  buffer[:Pkt_len]
                    buffer = buffer[Pkt_len:]
                    b_len = len(buff)

                    # print("buff[0]:",buff[0])
                    # print("buff[51]:",buff[51])

                    if ((buff[0] == '%') and (buff[51] == ']')): # 37 = %, 93 = ]
                        continue
                    else:
                        # decode Base64
                        collected_data = base64.b64decode(buff)
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
                    # print("buff:",buff)

                    if b_len == 0:
                        if (_debug):
                            print ('End of file')
                        break
                    if (buff[0] == '%'):     # '%' = 37
                        if (buff[1] == 'U' and buff[2] == 'U' and buff[3] == 'U'): # b'%UUU'
                            if (_debug):
                                print ("End of text")
                            # close file
                            f_out.close()

                            buff =  buffer[:4] # skip next four 'U's
                            buffer = buffer[4:]
                            
                            rcv_fn = []
                            i = 0
                            while (i < 44 and len(buffer) != 0):
                                ch = buffer[0]
                                buffer = buffer[1:]
                                if (ch == b'%'):
                                    break
                                rcv_fn.append((ch)) # (ord)(ch)
                                i += 1
                            rf_len = len (rcv_fn)
                            x = 0
                            while (x < rf_len):
                                rcv_fn[x] = str((rcv_fn[x]))
                                x += 1
                            ofn = "".join(rcv_fn)
                            if ("%UUU#EOF" in ofn):
                                index = ofn.index("%UUU#EOF")
                                ofn = ofn[:index]
                            print ("Transmitted file name:",ofn)

                            state = 2
                            working = False
                            continue
                    else:
                        # decode Base64
                        collected_data = base64.b64decode(buff)
                        # print("collected_data:")
                        if (_debug):
                            print(collected_data)
                        f_out.write (collected_data)
                        # print(f_out)

                        continue


            else:
                time.sleep(0.1) # wait 100ms and try again


    if (state == 2):
        # Open the image file
        print("Done stripping preamble")
        # time.sleep(3)

        # Attempt to open the image file
        try:
            with open(file_path, 'rb') as file:
                # contents = file.read()
                # print("Contents of file:")
                # print(contents)
                img = Image.open(file, mode='r')
                img.show()
                file.close()
        except:
            print('Could not open image file. Trying to open as text file...')
            try:
                with open(file_path, 'rb') as file:
                    contents = file.read()
                    print("Contents of file:")
                    print(contents)

                    file.close()
            except:
                print('Error: Could not open text file')

        # Prepare for next received file/image
        Pkt_len = 52
        state = 0
        buffer = ""
        working = True
        #exit(0)