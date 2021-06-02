#------------------------------------------------------------------------------------------------------------------
#   Real time processing of mobile sensor data.
#------------------------------------------------------------------------------------------------------------------
from subprocess import Popen
import sys
import time
import socket
# import struct
import numpy as np
# from scipy import stats
# from scipy import signal
import pickle
# from sklearn import svm, neighbors, tree
# from sklearn.model_selection import KFold
import keyboard
import threading

# Socket configuration
UDP_IP = '192.168.1.65'
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.001)

# Processing parameters
fs = 50                         # Sampling rate
win_length = 0.25               # Window length in seconds
win_samps = int(fs*win_length)  # Number of samples per window

# Data acquisition loop
data_buffer = []

start_time = time.time()
start_time2 = start_time
update_time = 0.25

# ('Tilt left', 1), ('Tilt right', 2), ('Tilt up', 3), ('Tilt down', 4)
movement = ['Left', 'Right', 'Up', 'Down']

with open('pickled_clf', 'rb') as pickled_clf:
    clf = pickle.load(pickled_clf)

print("The classifier was unpickled")

def send_data(features):
    # print(features)
    if features:
        x = np.array(features)
        y = clf.predict(x)
        direction = int(y)-1
        if direction == 0:
            # keyboard.press_and_release('left')
            print('SENDING LEFT')
        elif direction == 1:
            # keyboard.press_and_release('right')
            print('SENDING RIGHT')
        elif direction == 2:
            # keyboard.press_and_release('up')
            print('SENDING UP')
        elif direction == 3:
            # keyboard.press_and_release('down')
            print('SENDING DOWN')

# child = Popen([sys.executable, 'ai.py', '--username', 'root'])
# print('xdxdxdxdd')

try:
    while True:
            
        try:
            # Read data from UDP connection
            data, addr = sock.recvfrom(1024*1024)      

            # Decode binary stream. 
            data_string = data.decode('ascii').split(",")

            # Append new sensor data
            nsensors = (len(data_string)-1)/4

            for ind in range(1, len(data_string), 4):
                type =  int(data_string[ind])

                if type == 3:
                    data_buffer.append([float(data_string[ind+1]), float(data_string[ind+2]), float(data_string[ind+3])])

        except socket.timeout:
            pass

        ellapsed_time = time.time() - start_time;    
        if ellapsed_time > update_time and len(data_buffer) >= win_samps:

            start_time = time.time()        

            # Get last window
            win_data = np.array(data_buffer[-win_samps:])        
            nsignals = win_data.shape[1]
            # print('Last window', win_data)

            # Calculate features
            # The feature vector contains the following elements:
            # Avex, Stdx, Kurtosisx, Skewnesx, PSDx, Avey, Stdy, Kurtosisy, Skewnesy, PSDy, Avez, Stdz, Kurtosisz, Skewnesz, PSDz
            features = [[]]
            for k in range(nsignals):
                features[0].append(np.average(win_data[:,k]))
                # features.append(np.std(win_data[:,k]))
                # features.append(stats.kurtosis(win_data[:,k]))
                # features.append(stats.skew(win_data[:,k]))            
                
                # freqs, psd = signal.periodogram(win_data[:,k], fs, 'hamming', scaling='spectrum')            
                # features.extend(psd.tolist())

            #print('Features: ', features)
            send_data(features)
except KeyboardInterrupt:
    print('se acabo')

# child.wait()
# child.exit()


#------------------------------------------------------------------------------------------------------------------
#   End of file
#------------------------------------------------------------------------------------------------------------------