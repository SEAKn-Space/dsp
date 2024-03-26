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
