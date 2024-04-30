# SEAKn Space DSP Repository

Containing in this repo are several files involved and used in the Digital Signal Proccessing (DSP) side of our Capstone Design project.

Within this realm you can find source files for both our AI model and interacting with the Software Defined Radios (SDRs).

## AI Model

The main objective of our AI model is to be given complex data either directly from the SDR or from a data file and determine the modulation scheme used in that RF signal. 

The AI model uses a Convolution Neural Network (CNN) to determine the if the current modulation scheme of the signal is either a BPSK or QPSK signal. 

Additional documention on the AI model can be found in the Teams `Standard Work` folder.

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

This project was intended to have the AI model run on the Versal VCK190 using the onboard AI cores. The intended goal of everything working together was to have a seperate computer be able to send a BPSK or QPSK signal. That signal could then be received by another SDR and sent to the board or AI model to determine how the signal should be demodulated. 

## Transmit Side

After installing GNU Radio, a radio conda python instance should have been installed. This python environment is required to be run to include any GNU Radio blocks or flowgraphs to be run in the terminal. On Windows the default install location is `"C:/Users/user/radioconda/python.exe"`. The transmit side is intented to be run with the HackRF One connected to the computer. The automate_send&receive.py script is made to be run in a terminal and can run GNU Radio subprocesses that transmits either BPSK or QPSK. The script can continuously send either modulation scheme. To run the python script the following command can be run: `C:/Users/name/radioconda/python.exe "./SDR_files/board_interaction/automate_send&receive.py"` from the dsp parent directory. Make sure to change name in the filepath to the correct user.

A seperate file called `automate_with_buttons.py` was also created in the same board_interaction folder that can toggle between transmitting BPSK or QPSK signals using a push button. 

*Before running either script on a new computer with GNU Radio make sure to generate `bpsk_tx_automated.grc` and `qpsk_tx_automated.grc` found in the RX_TX folder or the script will fail to transmit.*

## Receive Side

#### Computer Side

A RTL-SDR is intended to be connected to receive the transmitted signal. The RTL-SDR should then be connected to a computer with GNU Radio installed. The computer should be connected to the board via an ethernet switch, which will be used to communicate between the board and the computer. The computer can then run `receive_chain.grc`. Within the flowchart there are two zmq socket blocks that will need to be modified to the computer's host IP.

![socket](https://github.com/SEAKn-Space/dsp/assets/125313875/d87a50a6-29d0-4d40-be15-049892a6ed49)

![socket1](https://github.com/SEAKn-Space/dsp/assets/125313875/cb271b5a-5664-4bcc-98eb-d24f6cf0bf2b)

There is one additional zmq socket block that can be kept as localhost (127.0.0.1). This block is intended to send the demodulated binary data to the `receive&display_message.py` script. This script will take the incoming binary data, strip the pre and post amble, and then try to display the image or print out the binary data received if an image cannot be opened.

![socket2](https://github.com/SEAKn-Space/dsp/assets/125313875/4a22abca-1908-4e54-aa64-a5e2869b1f23)

#### Board Side

Several steps were taken to transfer the AI model to the board, in which a more detailed instructions can be found located in the Teams `Standard Work` folder.

