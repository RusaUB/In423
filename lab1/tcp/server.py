import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 55000
BUFFER_SIZE = 1024
msg = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print('sending data...')
s.send(msg.encode('ascii'))

rawdata = s.recv(BUFFER_SIZE)
print("received data:\n", rawdata.decode('ascii'))

s.close()