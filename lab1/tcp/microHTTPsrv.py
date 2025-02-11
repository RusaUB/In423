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