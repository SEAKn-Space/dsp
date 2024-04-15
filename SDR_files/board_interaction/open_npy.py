import numpy as np

data = np.load("C:/Users/natha/dsp/SDR_files/board_interaction/calla.npy",allow_pickle=True) # load the file
print(len(data), type(data),data[0:10])
print(data)