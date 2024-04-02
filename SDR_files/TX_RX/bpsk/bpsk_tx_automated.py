#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: bpsk_tx_automated
# Author: SEAKn Space
# Description: packet transmit
# GNU Radio version: 3.10.8.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import bpsk_tx_automated_epy_block_0 as epy_block_0  # embedded python block




class bpsk_tx_automated(gr.top_block):

    def __init__(self, InFile='default'):
        gr.top_block.__init__(self, "bpsk_tx_automated", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.InFile = InFile

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100e3
        self.access_key = access_key = '11100001010110101110100010010011'
        self.transmit_freq = transmit_freq = 435e6
        self.sps = sps = 15
        self.rs_ratio = rs_ratio = 1.0
        self.packet_len = packet_len = 52
        self.low_pass_filter_taps = low_pass_filter_taps = firdes.low_pass(1.0, samp_rate, 20000,2000, window.WIN_HAMMING, 0.35)
        self.hdr_format = hdr_format = digital.header_format_default(access_key, 0)
        self.excess_bw = excess_bw = 0.35
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.bpsk.set_npwr(1.0)
        self.baseband_LO = baseband_LO = 0e3

        ##################################################
        # Blocks
        ##################################################

        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, 20*samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, transmit_freq)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(15, 0.0), 47.0))
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=20,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.epy_block_0 = epy_block_0.blk(FileName="./SDR_files/test_io/BPSK.png", Pkt_len=packet_len, initial_packet_fill=64)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=bpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "./ModulatedData.txt", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, baseband_LO, 0.3, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.epy_block_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.soapy_hackrf_sink_0, 0))


    def get_InFile(self):
        return self.InFile

    def set_InFile(self, InFile):
        self.InFile = InFile

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_low_pass_filter_taps(firdes.low_pass(1.0, self.samp_rate, 20000, 2000, window.WIN_HAMMING, 0.35))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, 20*self.samp_rate)

    def get_access_key(self):
        return self.access_key

    def set_access_key(self, access_key):
        self.access_key = access_key
        self.set_hdr_format(digital.header_format_default(self.access_key, 0))

    def get_transmit_freq(self):
        return self.transmit_freq

    def set_transmit_freq(self, transmit_freq):
        self.transmit_freq = transmit_freq
        self.soapy_hackrf_sink_0.set_frequency(0, self.transmit_freq)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.epy_block_0.Pkt_len = self.packet_len

    def get_low_pass_filter_taps(self):
        return self.low_pass_filter_taps

    def set_low_pass_filter_taps(self, low_pass_filter_taps):
        self.low_pass_filter_taps = low_pass_filter_taps

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk

    def get_baseband_LO(self):
        return self.baseband_LO

    def set_baseband_LO(self, baseband_LO):
        self.baseband_LO = baseband_LO
        self.analog_sig_source_x_0.set_frequency(self.baseband_LO)



def argument_parser():
    description = 'packet transmit'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--InFile", dest="InFile", type=str, default='default',
        help="Set File Name [default=%(default)r]")
    return parser


def main(top_block_cls=bpsk_tx_automated, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(InFile=options.InFile)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
