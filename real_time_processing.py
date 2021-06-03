#------------------------------------------------------------------------------------------------------------------
#   Real time processing of mobile sensor data.
#------------------------------------------------------------------------------------------------------------------
import time
import socket
import numpy as np
import pickle


# Socket configuration
PHONE_CONN_ADDR = ('192.168.1.65', 8000)
GAME_CONN_ADDR = ('localhost', 8001)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(PHONE_CONN_ADDR)
sock.settimeout(0.001)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.connect(GAME_CONN_ADDR)
print('connected to server!')

# Processing parameters
fs = 10                         # Sampling rate
win_length = 0.1                # Window length in seconds
win_samps = int(fs*win_length)  # Number of samples per window

# Data acquisition loop
data_buffer = []

start_time = time.time()
start_time2 = start_time
update_time = 0.05

# ('Tilt left', 1), ('Tilt right', 2), ('Tilt up', 3), ('Tilt down', 4)
movement = ['Left', 'Right', 'Up', 'Down']

# The classifier is unpickled
with open('pickled_clf', 'rb') as pickled_clf:
    clf = pickle.load(pickled_clf)

def send_data(features):
    # print(features)
    if features:
        x = np.array(features)
        y = clf.predict(x)
        direction = int(y)-1
        if direction == 0:
            # keyboard.press_and_release('left')
            print('SENDING LEFT')
            sock2.send(b'0')
        elif direction == 1:
            # keyboard.press_and_release('right')
            print('SENDING RIGHT')
            sock2.send(b'1')
        elif direction == 2:
            # keyboard.press_and_release('up')
            print('SENDING UP')
            sock2.send(b'2')
        elif direction == 3:
            # keyboard.press_and_release('down')
            print('SENDING DOWN')
            sock2.send(b'3')
        else:
            print('No features!!')

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

        except socket.timeout as etime:
            # sock.close()
            # print(str(etime))
            # sys.exit()
            pass

        ellapsed_time = time.time() - start_time;    
        if ellapsed_time > update_time and len(data_buffer) >= win_samps:

            start_time = time.time()        

            # Get last window
            win_data = np.array(data_buffer[-win_samps:])        
            nsignals = win_data.shape[1]
            features = [[]]
            for k in range(nsignals):
                features[0].append(np.average(win_data[:,k]))

            send_data(features)
except (KeyboardInterrupt, ConnectionResetError):
    sock.close()
    print('Game!')
#------------------------------------------------------------------------------------------------------------------
#   End of file
#------------------------------------------------------------------------------------------------------------------