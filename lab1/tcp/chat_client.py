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