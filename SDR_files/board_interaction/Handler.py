import os
import subprocess

# Create a named pipe (FIFO)
fifo_path = "my_fifo.pipe"
os.mkfifo(fifo_path)

# Start the producer program (replace "producer_command" with the actual command to run your producer program)
producer_process = subprocess.Popen(['python', './SDR_files/TX_RX/qpsk/qpsk_txrx.py' ], stdout=subprocess.PIPE)
# producer_process = subprocess.Popen(['python', './SDR_files/board_interaction/radio2File.py' ], stdout=subprocess.PIPE)


# Start the consumer program (replace "consumer_command" with the actual command to run your consumer program)
consumer_process = subprocess.Popen(['python','./SDR_files/board_interaction/qpsk_rx_fileRead.py', fifo_path])

# Read output from the producer and write to the named pipe
with open(fifo_path, "wb") as fifo:
    for line in producer_process.stdout:
        fifo.write(line)
        fifo.flush()  # Ensure data is immediately written to the pipe

# Wait for the consumer to finish
consumer_process.wait()

# Cleanup: Close and remove the named pipe
os.remove(fifo_path)
