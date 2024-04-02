"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """'Demodulation Scheme Select From Board'"""

    def __init__(self, demod_selector=True):  # only default arguments here
        """'Demodulation Scheme Select From Board'"""
        gr.sync_block.__init__(
            self,
            name='Demodulation Scheme Select From Board',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.portName = "demod_select"
        self.message_port_register_out(pmt.intern(self.portName))

        self.demod_selector = demod_selector

    def work(self, input_items, output_items):
        
        print("Random number: ", rand)
        rand = np.random.randint(2)
        time.sleep(0.1)
        self.demod_selector = rand
        PMT_msg = pmt.from_bool(self.rand)
        self.message_port_pub(pmt.intern(self.portName), PMT_msg)

        return (input_items[0])

    # def handle_msg(self, msg):
    #     self.selector = pmt.to_bool(msg)