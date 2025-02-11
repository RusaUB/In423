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