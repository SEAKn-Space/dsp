import subprocess
import random
import math
import msvcrt
import keyboard

choice = 1

#Callback for when the button is pressed
def button_press(tmp):
    global choice
    choice = not(choice)
    if choice:
        print("Transmitting BPSK")
        tranmit_bpsk
    else:
        print("Transmitting QPSK")
        tranmit_qpsk


# Run QPSK transmit
def tranmit_qpsk():
    subprocess.run(['python', './SDR_files/TX_RX/qpsk/qpsk_tx_automated.py' ])

# Run BPSK transmit
def tranmit_bpsk():
    subprocess.run(['python',  './SDR_files/TX_RX/bpsk/bpsk_tx_automated.py' ])

print("Press Button to Begin Transmission")
print("Press Again to Toggle")

try:
    while(1):
        if keyboard.is_pressed('space'):
            keyboard.on_release_key('space',button_press,suppress=True)
except KeyboardInterrupt:
    print("Exiting")        