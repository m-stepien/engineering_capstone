import cv2
import socket
import pickle
import numpy as np  

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
# inz.local
host_ip = 'localhost'
port = 12346

client_socket.bind(('', port)) 
print(f"Client ready to receive video from {host_ip}:{port}")

try:
    while True:
        data, addr = client_socket.recvfrom(65536)
        frame = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        if image is not None:
            cv2.imshow("Video", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
except Exception as e:
    print(f"Error: {e}")
finally:
    cv2.destroyAllWindows()
    client_socket.close()