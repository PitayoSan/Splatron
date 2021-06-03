# server
import socket

HOST = 'localhost'
PORT = 8009

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

conn, addr = s.accept()
try:

    with conn:
        print(addr, ' connected')
        while True:
            data = conn.recv(1024)
            if data:
                #print('received: ', data)
                #conn.send(data)
                print(data)
except KeyboardInterrupt:
    s.close()