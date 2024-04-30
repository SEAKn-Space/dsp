# SDR Files
This folder contains files that relate to using and interacting and using the SDRs for this project. 

# Folder and File Descriptions

## TX_RX

Files within TX_RX are intended to be used with the SDRs connected to the current device that can run GNU Radio. A HackRF One is intended for any transmitting (tx) and an RTL-SDR is intended for any receiving (rx). The bpsk and qpsk folder contains GNU Radio Flowcharts (grc) files that can either transmit, receive, or both in the selected modulated scheme. 8psk and FM folders can also be found within this folder but were not as heavily tested or is guaranteed to work.

## TX_RX_Simulation

Files within TX_RX_Simulation are intended to be used without SDRs connected to the current device that can run GNU Radio.

## board_interaction

The board_interaction folder contains many helper functions or python scripts that can or need be run to faciliate communication between the VCK190 and computer. 

## test_io

Contains test io files such as images or text files that can be used to transmit. This is also the default folder location for the binary output to be saved to after message is demodulated (out_File). 
