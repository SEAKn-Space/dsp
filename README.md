# SEAKn Space DSP Repository

Containing in this repo are several files involved and used in the Digital Signal Proccessing (DSP) side of our Capstone Design project.

Within this realm you can find source files for both our AI model and interacting with the Software Defined Radios (SDRs).

## AI Model

The main objective of our AI model is to be given complex data either directly from the SDR or from a data file and determine the modulation scheme used in that RF signal. 

The AI model currently uses a Convolution Neural Network (CNN) to determine the current if the current modulation scheme is either a BPSK or QPSK signal. On going progress to improve this model and potentiall add more modulation schemes to determine between.  

## SDR files

For this project two SDRs were used. A HackRF One is used to transmit the modulated signal while a RTL-SDR is used as a receiver to collect the transmitted data to feed into the AI model. 

Some pre and post processing will be neccesary to allow the model to chose the appropriate modulation scheme and then begin demodulation. *Current work in progress*

For the most part, most interactin with the SDRs is done through the use of GNU Radio and their associated python scripts. Within the SDR folder two sub-folders can be found. The RX_TX files are designed to work on the aforementioned SDRs to actually send (TX) and receive (RX) the modulated signals. The RX_TX_simulation folder contains the same GNU Radio files but can be simulated on the computer to transmit and recieve without using any SDRs.

### GNU Radio Download and Other Dependencies

To install GNU Radio, download instructions can be found [here](https://wiki.gnuradio.org/index.php/InstallingGR).

To install all needed python library dependencies run `pip install -r requirements.txt`. 

### GNU Radio Block Design and Further Resources

To help make the different block diagrams, official [wiki tutorials](https://wiki.gnuradio.org/index.php?title=Tutorials) were used. 

For PSK modulation specifically and packet formatting protocol, a [tutorial on packets](https://wiki.gnuradio.org/index.php?title=File_transfer_using_Packet_and_BPSK) proved helpful, as well as using an [online guide from Nuclearrando](https://nuclearrambo.com/wordpress/transferring-a-text-file-over-the-air-with-limesdr-mini/) to help debug and fix some of the issues with using the hardware SDRs.

### Running SDR Files

After installing GNU Radio, a radio conda python instance should have been installed. This python environment is required to be run to include any GNU Radio blocks or flowgraphs to be run in the terminal. On Windows the default install location is `"C:/Users/user/radioconda/python.exe"`.

### Full Send and Receive Pipeline

Two main python scripts can be run, one on the transmit side and one on the receive side. 

#### Transmit Side

The transmit side is intented to be run with the HackRF One connected to the computer. The automate_send&receive.py script is made to be run in a terminal and can run GNU Radio subprocesses that transmits either BPSK or QPSK. The script can continuously send either modulation scheme. To run the python script the following command can be run: `C:/Users/name/radioconda/python.exe "c:/Users/name/dsp/SDR_files/board_interaction/automate_send&receive.py"`. Make sure to change name in the filepath to the correct user.

#### Receive Side

The receive side is intended to be run with a RTL-SDR connected to the computer. The receive side is a GNU Radio flowgraph that makes an output file that will be send to the board. The flowgraph also takes is a message from the board to switch between demodulation BPSK or QPSK.

# Putting Everything Together

This project was intended to have the AI model run on the Versal VCK190 using the onboard AI cores. The intended goal of everything working together was to have a seperate computer be able to send a BPSK or QPSK signal. That signal could then be received by the other SDR and sent to the board or AI model to determine how the signal should be demodulated. 

## Transmit Side

The transmit side is intented to be run with the HackRF One connected to the computer. The automate_send&receive.py script is made to be run in a terminal and can run GNU Radio subprocesses that transmits either BPSK or QPSK. The script can continuously send either modulation scheme. To run the python script the following command can be run: `C:/Users/name/radioconda/python.exe "c:/Users/name/dsp/SDR_files/board_interaction/automate_send&receive.py"`. Make sure to change name in the filepath to the correct user.

## Receive Side
