# client
import socket
import sys

HOST = 'localhost'
PORT = 8009

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


try:
    while True:
        msg = input('Say something: ')
        s.send(bytes(msg, 'utf-8'))
except KeyboardInterrupt:
    s.close()
    sys.exit()