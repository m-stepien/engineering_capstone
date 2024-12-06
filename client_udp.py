import cv2
import socket
import pickle
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
host_ip = '192.168.0.154'
port = 12346

client_socket.bind(('', port)) 
print(f"Client ready to receive video from {host_ip}:{port}")

try:
    while True:
        packet, _ = client_socket.recvfrom(65535) 
        data = pickle.loads(packet)


        frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

        cv2.imshow('Client: Video Stream', frame)
        if cv2.waitKey(1) == 27:  
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    cv2.destroyAllWindows()
    client_socket.close()