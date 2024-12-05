import cv2
import socket
import pickle
import numpy as np

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
host_ip = 'inz.local'
port = 12346

client_socket.bind(('', port))  # Bind to any IP for receiving
print(f"Client ready to receive video from {host_ip}:{port}")

try:
    while True:
        # Receive data
        packet, _ = client_socket.recvfrom(65535)  # Max UDP packet size
        data = pickle.loads(packet)

        # Decode the frame
        frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

        # Display the frame
        cv2.imshow('Client: Video Stream', frame)
        if cv2.waitKey(1) == 27:  # Press Esc to exit
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    cv2.destroyAllWindows()
    client_socket.close()