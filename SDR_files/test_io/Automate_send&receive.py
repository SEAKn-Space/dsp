import subprocess
import random
import math
import msvcrt

# Run QPSK transmit
def tranmit_qpsk():
    subprocess.run(['python', '../TX_RX/qpsk/qpsk_tx_automated.py' ])

# Run BPSK transmit
def tranmit_bpsk():
    subprocess.run(['python',  '../TX_RX/bpsk/bpsk_tx_automated.py' ])

# Transmit random signal
def tranmit_random():
    rand = math.floor(random.random()*2)
    if rand == 0:
        print("Transmitting random signal... BPSK chosen...")
        tranmit_bpsk()
    elif rand == 1:
        print("Transmitting random signal... QPSK chosen...")
        tranmit_qpsk()

print("Welcome to Automated Send!")
print("Make sure to have HackRF connected before running.")
print("Select a modulation scheme to transmit. Use 'help' for a list of commands.")
# Main terminal loop
while(1):

    input_str = input("Enter command: ")

    if input_str.upper() == "QPSK":
        print("Transmitting QPSK signal...")
        tranmit_qpsk()
    elif input_str.upper() == "BPSK":
        print("Transmitting BPSK signal...")
        tranmit_bpsk()
    elif input_str.upper() == "RAND" or input_str.upper() == "RANDOM":
        tranmit_random()
    elif input_str.upper() == "CONT" or input_str.upper() == "CONTINUOUS":
        print("Press any key to stop continuous transmission.")
        while(1):
            tranmit_random()
            if msvcrt.kbhit():
                break
    elif input_str.upper() == "CONTBPSK":
        print("Press any key to stop continuous transmission.")
        while(1):
            print("Transmitting BPSK signal...")
            tranmit_bpsk()
            if msvcrt.kbhit():
                break
    elif input_str.upper() == "CONTQPSK":
        print("Press any key to stop continuous transmission.")
        while(1):
            print("Transmitting QPSK signal...")
            tranmit_qpsk()
            if msvcrt.kbhit():
                break
    elif input_str.upper() == "EXIT":
        exit(0)
    elif input_str.upper() == "HELP" or input_str.upper() == "?":
        print("Commands:")
        print("QPSK - Transmit Quadrature Phase Shift Keying Signal")
        print("BPSK - Transmit Binary Phase Shift Keying Signal")
        print("rand - send a random signal")
        print("cont - continuously send a random signal")
        print("contbpsk - continuously send a BPSK signal")
        print("contqpsk - continuously send a QPSK signal")
        print("help - display this message")
        print("exit - exit the program")
    else:
        print("Invalid command. Use 'help' for a list of commands.")