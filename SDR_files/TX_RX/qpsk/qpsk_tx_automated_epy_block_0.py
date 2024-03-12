"""
Embedded Python Block: File Source to Tagged Stream
"""

import numpy as np
from gnuradio import gr
import time
import pmt
import os.path
import sys
import base64
import math

"""
State definitions
    0   idle
    1   send preamble
    2   send file data
    3   send file name
    4   send post filler
"""

class blk(gr.sync_block):
    def __init__(self, FileName='None', Pkt_len=52, initial_packet_fill=1):
        gr.sync_block.__init__(
            self,
            name='EPB: File Source to Tagged Stream',
            in_sig=None,
            out_sig=[np.uint8])
        self.FileName = FileName
        self.Pkt_len = Pkt_len
        self.initial_packet_fill = initial_packet_fill
        self.state = 0      # idle state
        self.pre_count = 0
        self.indx = 0
        self._debug = 0     # debug
        self.data = ""

        if (os.path.exists(self.FileName)):
            # open input file
            self.f_in = open (self.FileName, 'rb')
            self._eof = False
            if (self._debug):
                print ("File name:", self.FileName)
            self.state = 1
        else:
            print(self.FileName, 'does not exist')
            self._eof = True
            self.state = 0

        self.char_list = [37,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,93]
        self.c_len = len (self.char_list)
        # print (self.c_len)
        self.filler = [37,85,85,85, 35,69,79,70, 85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,93]
        self.f_len = len (self.filler)

    def work(self, input_items, output_items):

        # Attempt at fixing buffer overflow
        if(len(output_items[0])<(int(math.ceil(self.Pkt_len*8/6)))):
            if (self._debug):
                print("GNU Radio Buffer Overflow")
                print("Try Decreasing Input File Size or Increasing Minoutput Buffer")
            return 0

        if (self.state == 0):
            if (self._debug):
                print("State 0")
            # idle
            return -1

        elif (self.state == 1):
            # send preamble
            if (self._debug):
                print ("State = 1", self.pre_count)
            key1 = pmt.intern("packet_len")
            val1 = pmt.from_long(self.c_len)
            self.add_item_tag(0, # Write to output port 0
                self.indx,   # Index of the tag
                key1,   # Key of the tag
                val1    # Value of the tag
                )
            self.indx += self.c_len
            
            i = 0
            j = 0
            while(j<self.initial_packet_fill*self.c_len):
                i = 0
                while (i < self.c_len):
                    output_items[0][j] = self.char_list[i]
                    i += 1
                    j += 1
                
                self.pre_count += 1


            if (self.pre_count > 64):
                self.pre_count = 0
                self.state = 2      # send msg
            return (self.c_len)

        elif (self.state == 2):
            if (self._debug):
                print("State 2")
            while (not (self._eof)):
                buff = self.f_in.read(self.Pkt_len)
                b_len = len(buff)
                # if (self._debug):
                #     print ('buff length =', b_len, 'buff:', buff)
                if b_len == 0:
                    # print ('End of file')
                    self._eof = True
                    self.f_in.close()
                    self.state = 3      # send file name
                    self.pre_count = 0
                    break
                # convert to Base64
                encoded = base64.b64encode (buff)
                e_len = len(encoded)
                # if (self._debug):
                #     print ('b64 length =', e_len)
                #     print('encoded:', encoded)
                key0 = pmt.intern("packet_len")
                val0 = pmt.from_long(e_len)
                self.add_item_tag(0, # Write to output port 0
                    self.indx,   # Index of the tag
                    key0,   # Key of the tag
                    val0    # Value of the tag
                    )
                self.indx += e_len

                if (self._debug):
                    # print ("Length of input:",len(input_items[0]))                    
                    print ("Length of output:",len(output_items[0]))


                i = 0
                while (i < len(encoded) and len(output_items[0])>=len(encoded)):
                    # if (i == 63):
                    #     print("i",encoded[i])
                    output_items[0][i] = encoded[i]
                    # print("i",i)
                    i += 1

                if(len(output_items[0])<len(encoded)):
                    print("GNU Radio Buffer Overflow")
                    print("Try Decreasing Input File Size or Increasing Minoutput Buffer")
                    return 0
                return (e_len)

        elif (self.state == 3):
            if (self._debug):
                print("State 3")
            # send file name
            fn_len = len (self.FileName)
            key1 = pmt.intern("packet_len")
            val1 = pmt.from_long(fn_len+8)
            self.add_item_tag(0, # Write to output port 0
                self.indx,   # Index of the tag
                key1,   # Key of the tag
                val1    # Value of the tag
                )
            self.indx += (fn_len+8)
            i = 0
            while (i < 8):
                output_items[0][i] = self.filler[i]
                i += 1
            j = 0
            while (i < (fn_len+8)):
                output_items[0][i] = ord(self.FileName[j])
                i += 1
                j += 1
            self.state = 4
            return (fn_len+8)

        elif (self.state == 4):
            # send post fillers
            if (self._debug):
                print ("State = 4 , precount =", self.pre_count)
            key1 = pmt.intern("packet_len")
            val1 = pmt.from_long(self.f_len)
            self.add_item_tag(0, # Write to output port 0
                self.indx,   # Index of the tag
                key1,   # Key of the tag
                val1    # Value of the tag
                )
            self.indx += self.f_len
            
            i = 0
            while (i < self.f_len):
                output_items[0][i] = self.filler[i]
                i += 1
            self.pre_count += 1
            if (self.pre_count > 16):
                self.pre_count = 0
                self.state = 0      # idle
            return (self.f_len)

        return (0)
