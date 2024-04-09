from xmlrpc.client import ServerProxy
import time

xmlrpc_control_client = ServerProxy('http://'+'localhost'+':8080')
demod_choices = [0, 1] # BPSK=0, QPSK=1

print("Chose Modulation Scheme to Demodulate")
print("BPSK=0, QPSK=1")
while True:
    demod_choice = int(input("Enter modulation scheme: "))
    if demod_choice in demod_choices:
        if(demod_choice == 0):
            print("Demodulating BPSK signal...")
        else:
            print("Demodulating QPSK signal...")
        xmlrpc_control_client.set_demod_selector(demod_choice)
    else:
        print("Invalid choice. Please try again.")