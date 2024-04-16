"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import os
import subprocess
import multiprocessing
from gnuradio import gr
import sys
sys.path.append("C:/Users/natha/dsp/SDR_files/board_interaction")
from random import randint
from Handler import main as Handler

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Data To STD_out',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=None,
        )
        # print("Data Starts Here:") # print to STDOUT that the data starts here
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        # self.example_param = example_param

        # Start prodicer/handler process
        self.queue = multiprocessing.Queue() # Create queue to send data to handler
        # handler_process = multiprocessing.Process(target=self.handler, args=(self.queue,))
        multiprocessing.Process(target=Handler, args=(self.queue,)).start()
        # handler_process = subprocess.Popen(['python','./SDR_files/board_interaction/qpsk_rx_fileRead.py', self.queue])


    def work(self, input_items, output_items): # work(self, input_items, output_items):
        """example: multiply with constant"""
        # print(input_items) # print to STDOUT the file data
        # print(type(input_items))
        
        mystery_num = randint(1,1_000_000)
        # print("Mystery Number: " + str(mystery_num))
        if(mystery_num == 1):
            print("Sending data to handler...")
            self.queue.put(np.asarray(input_items))

        return 0
