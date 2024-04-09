"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import random
from gnuradio import gr

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block - Randomly grab 128 samples and save to file or pass onto next block."""

    def __init__(self, save_file="calla.np", num_points=128):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            # out_sig=None,
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.save_file = save_file 
        self.num_points = num_points

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0] = np.array([0], dtype=np.complex64)



        mystery_num = random.randint(1,1_000)
        if(mystery_num == 1):
            # print("Data ,", input_items[0])
            # print(type(input_items))
            # print(len(input_items))
            if (len(input_items[0]) >= self.num_points):
                start = random.randint(0, len(input_items[0])-self.num_points)
                data = input_items[0][start:start+self.num_points]
                output_items[0] = data
                # print(data)
                print("Collected {} samples".format(len(data)))
                # data.tofile(self.save_file)
                np.save(self.save_file, data, allow_pickle=True)
                
        return len(input_items[0])
        # return (len(output_items[0]))