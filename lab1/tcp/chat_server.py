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