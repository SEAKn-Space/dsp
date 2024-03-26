"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import os
import subprocess
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Data To STD_out',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=None
        )
        # print("Data Starts Here:") # print to STDOUT that the data starts here
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        # self.example_param = example_param

    def work(self, input_items, output_items): # work(self, input_items, output_items):
        """example: multiply with constant"""
        print(input_items) # print to STDOUT the file data
        return 0
