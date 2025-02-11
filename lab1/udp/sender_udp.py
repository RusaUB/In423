import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
message = "Hello, World!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message.encode("utf-8"), (UDP_IP, UDP_PORT))