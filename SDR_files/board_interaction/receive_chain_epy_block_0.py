"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import random
from gnuradio import gr
import torch

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block - Randomly grab num_points samples and save to file or pass onto next block.
    Args:
        save_file (str): File to save samples to. Set to None to not save to file.
        num_points (int): Number of samples to grab. Ex: 128. Must be less than or equal to the number of samples in the input (4096).
        grab_random (bool): If True, grab samples randomly. If False, grab samples sequentially at given rate.
        rate (int): Rate at which to grab samples. Higher rate means longer time between grabbing samples.
        debug (bool): If True, print debug messages."""

    def __init__(self, save_file="calla.np", num_points=128, grab_random=False, rate=10_000,debug=False):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Get Random Sample',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.save_file = save_file 
        self.num_points = num_points
        self.grab_random = grab_random
        self.rate = rate
        self._debug = debug

        self.iter_counts = 0

    def work(self, input_items, output_items):
        """Grab num_points samples and save to file or pass onto next block."""

        if (input_items is None or len(input_items[0]) is None or input_items[0] is None):
            print("Input type is None")
            return 0

        if self.grab_random:
            mystery_num = random.randint(1,self.rate)
            if(mystery_num == 1):
                self.iter_counts = 0
                if (len(input_items[0]) >= self.num_points):
                    start = random.randint(0, len(input_items[0])-self.num_points)
                    data = input_items[0][start:start+self.num_points]
                    output_items[0][:len(data)] = input_items[0][start:start+self.num_points]

                    if self._debug:
                        print("Collected {} samples".format(len(data), type(input_items[0]), output_items[0][:] ))
                    
                    # save to file
                    if not self.save_file is None:
                        np.save(self.save_file, data, allow_pickle=True)
                    return len(data)
                elif self._debug:
                    print("Input length is less than num_points")
            
        else:
            self.iter_counts += 1
            if (self.iter_counts >= self.rate):

                self.iter_counts = 0
                if self._debug:
                    print("Input length: ",len(input_items[0]))

                if (int(len(input_items[0])) >= int(self.num_points)):
                    start = random.randint(0, len(input_items[0])-self.num_points)
                    data = input_items[0][start:start+self.num_points]
                    output_items[0][:len(data)] = input_items[0][start:start+self.num_points]
                    if self._debug:
                        print("Collected {} samples".format(len(data), type(input_items[0]), output_items[0][:] ))
                    
                    formated_data = np.vstack((data.real, data.imag))
                    formated_data_torch = torch.from_numpy(formated_data)
                    formated_data_tensor = torch.tensor(formated_data_torch, dtype=torch.float32)
                    min_val = torch.tensor(formated_data_tensor.min(axis=1).values, dtype=torch.float32)
                    max_val = torch.tensor(formated_data_tensor.max(axis=1).values, dtype=torch.float32)

                    #normalize
                    epsilon = 1e-10
                    normalized_data = 2* (formated_data_tensor - min_val.unsqueeze(1)) / (max_val.unsqueeze(1) - min_val.unsqueeze(1) + epsilon) - 1
                    normalized_data_np = normalized_data.numpy()
                    
                    if self._debug:
                        print(normalized_data_np.shape)
                        print(formated_data.shape)
                        print(formated_data[0:10])

                    # save to file
                    if not self.save_file is None:
                        np.save(self.save_file, data, allow_pickle=True)
                    return len(data)
                elif self._debug:
                    print("Input length is less than num_points")

        output_items[0][:] = 0
        return self.num_points
        # output_items[0][:self.num_points] = input_items[0][:self.num_points]
        # return (len(output_items[0]))