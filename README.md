
# **IN423 - Networking Labs**

## **LAB 1 - UDP & TCP Communication**

### **Objectives**
The objective of this lab is to explore data exchange over standard computer networks using **UDP** and **TCP** sockets in Python. The exercises include:

- Creating a simple **chat application** using UDP and TCP sockets.
- Implementing a **micro HTTP server** to handle requests.
- Processing and decoding **drone data** sent over UDP.

---

## **1. UDP Communication**

UDP (User Datagram Protocol) is a connectionless communication protocol that allows for fast data transmission. However, it does not guarantee message delivery, order, or error checking.

### **1.1 UDP Sender and Receiver**

#### **UDP Server (Receiver)**
The UDP server listens for incoming messages and prints the received data along with the sender's address.

```python
import socket

# Define the server IP and port
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP and port
sock.bind((UDP_IP, UDP_PORT))

print(f"UDP Server listening on {UDP_IP}:{UDP_PORT}...")

# Receive messages in a loop
while True:
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    print(f"Received message: {data.decode('utf-8')}")
    print(f"From address: {addr}")

```

#### **UDP Client (Sender)**

The UDP client sends a message to the server.

```python
import socket

# Define the server IP and port
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
message = "Hello, World!"

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a message to the server
sock.sendto(message.encode("utf-8"), (UDP_IP, UDP_PORT))

print(f"Message sent: {message}")

```

**💡 How it works:**

1.  Run the **UDP server script** first.
2.  Then, execute the **UDP client script** to send a message.
3.  The server should display the received message and the sender’s address.

----------

## **2. Drone Data Frame over UDP**

Drones often send telemetry data using UDP in a structured binary format. This example demonstrates how to receive and decode drone data packets using **Python’s `struct` module**.

### **2.1 Understanding the Drone Data Format**

| Field        | Data Type | Size (bytes) | Description                    |
|--------------|-----------|--------------|--------------------------------|
| **Date**     | `double`  | 8            | Timestamp of the data          |
| **Pitch**    | `int`     | 4            | Pitch angle of the drone       |
| **Roll**     | `int`     | 4            | Roll angle of the drone        |
| **Yaw**      | `int`     | 4            | Yaw angle of the drone         |
| **Battery**  | `int`     | 4            | Battery percentage             |
| **Barometer**| `float`   | 4            | Atmospheric pressure           |
| **AGX**      | `float`   | 4            | Acceleration in X direction    |
| **AGY**      | `float`   | 4            | Acceleration in Y direction    |
| **AGZ**      | `float`   | 4            | Acceleration in Z direction    |


### **2.2 Implementing the Drone Data Receiver**

The following script listens for drone telemetry data on multiple UDP ports and decodes it for display.

```python
import socket
import struct
import datetime
import select

BROADCAST_IP = "192.168.1.255"
PORTS = [52001, 52002]

class RemoteSensors:
    def __init__(self, udp_ip, ports):
        self.UDP_IP = udp_ip
        self.sockets = []
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.UDP_IP, port))
            self.sockets.append(sock)

    """

    The data from the drone are transmited as raw bytes, i.e. not in text encoding and follow this description :

    -> date (8 bytes double float) d
    -> pitch (4 bytes int) i
    -> roll (4 bytes int) i
    -> yaw (4 bytes int) i
    -> battery (4 bytes int)  i
    -> barometer (4 bytes single float) f
    -> agx (4 bytes single float) f
    -> agy (4 bytes single float) f
    -> agz (4 bytes single float) f
    
    """
    def decode_drone_data(self, data):
        decoded_data = struct.unpack('diiiiffff', data[0:40])
        return {
            'date': datetime.datetime.fromtimestamp(decoded_data[0]),
            'pitch': decoded_data[1],
            'roll': decoded_data[2],
            'yaw': decoded_data[3],
            'battery': decoded_data[4],
            'barometer': decoded_data[5],
            'agx': decoded_data[6],
            'agy': decoded_data[7],
            'agz': decoded_data[8]
        }
    
    def print_drone_data(self, data_dict):
        for key, value in data_dict.items():
            print(f"{key}: {value}")
        print("-" * 50)


    """
    Usage of two sockets with the select function to be able to read the two streams for the samer script
    """
    
    def listen(self):
        while True:
            readable, _, _ = select.select(self.sockets, [], [])
            
            for sock in readable:
                try:
                    data, addr = sock.recvfrom(1024)
                    port = sock.getsockname()[1]
                    
                    print(f"\nReceived message on port {port} from {addr}:")
                    
                    if port == 52001:  
                        try:
                            decoded_data = self.decode_drone_data(data)
                            self.print_drone_data(decoded_data)
                        except struct.error:
                            print("Error decoding drone data")
                    else:  
                        try:
                            message = self.decode_drone_data(data)
                            print(f"Message: {message}")
                        except UnicodeDecodeError:
                            print("Error decoding message as ASCII")
                            
                except Exception as e:
                    print(f"Error receiving data: {e}")

def main():    
    sensors = RemoteSensors(BROADCAST_IP, PORTS)
    print(f"Listening on {BROADCAST_IP} ports {PORTS}...")
    sensors.listen()

if __name__ == "__main__":
    main()

```

# TCP Examples

## 1. Basic TCP Echo Server and Client

### TCP Server

```python
import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 55000
BUFFER_SIZE = 1024

sconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sconn.bind((TCP_IP, TCP_PORT))
print(f'binding to {TCP_IP}:{TCP_PORT}')
sconn.listen(1)

s, addr = sconn.accept()
rawdata = s.recv(BUFFER_SIZE)
print("received data:", rawdata.decode('ascii'))
s.send(rawdata)

s.close()
sconn.close()
```

### TCP Client

```python
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
```

---

## 2. MiniChat

### Chat Client

```python
import socket
import threading
import sys

class ChatClient:
    def __init__(self, host="127.0.0.1", port=55000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connected to server")
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.send_messages()
            
        except Exception as e:
            print(f"Error connecting to server: {e}")
            sys.exit(1)
    
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    print("\nDisconnected from server")
                    sys.exit(0)
                print(f"\nReceived: {message}")
                print("Your message: ", end='', flush=True)
            except Exception as e:
                print(f"\nError receiving message: {e}")
                self.client_socket.close()
                sys.exit(1)
    
    def send_messages(self):
        try:
            while True:
                message = input("Your message: ")
                if message.lower() == 'quit':
                    break
                self.client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        finally:
            self.client_socket.close()
            sys.exit(0)

if __name__ == "__main__":
    client = ChatClient()
    client.start()
```

### Chat Server

```python
import socket
import threading

class ChatServer:
    def __init__(self, host="127.0.0.1", port=55000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"New connection from {address}")
            self.clients.append(client_socket)
            
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, address)
            )
            client_thread.start()
    
    def handle_client(self, client_socket, address):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                print(f"Message from {address}: {message}")
                
                self.broadcast(message, client_socket)
                
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()
            print(f"Connection from {address} closed")
    
    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.clients.remove(client)
                    client.close()

if __name__ == "__main__":
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        for client in server.clients:
            client.close()
        server.server_socket.close()
```

---

## 3. HTTP Server

```python
import socket
import threading
import time

class HTTPServer:
    def __init__(self, host="127.0.0.1", port=55000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on http://{self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"New connection from {address}")
            
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, address)
            )
            client_thread.start()
    
    def create_http_response(self):
        http_head = "HTTP/1.1 200 OK\r\n"
        http_head += "Date:" + time.asctime() + " GMT\r\n"
        http_head += "Expires: -1\r\n"
        http_head += "Cache-Control: private, max-age=0\r\n"
        http_head += "Content-Type: text/html;"
        http_head += "charset=utf-8\r\n"
        http_head += "\r\n"
        
        data = "<html><head><meta charset='utf-8'/></head>"
        data += "<body><h1>In43 is the best course ! ÉÇ </h1>"
        data += "</body></html>\r\n"
        data += "\r\n"
        
        return http_head.encode("ascii") + data.encode("utf-8")
    
    def handle_client(self, client_socket, address):
        try:
            # Receive HTTP request
            request = client_socket.recv(1024).decode('utf-8')
            if request:
                print(f"HTTP Request from {address}:")
                print(request)
                
                # Send HTTP response
                http_response = self.create_http_response()
                client_socket.send(http_response)
                
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection from {address} closed")

if __name__ == "__main__":
    server = HTTPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_socket.close()
```
