import cv2
import socket
import pickle
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_ip = '0.0.0.0'  
port = 12346
server_socket.bind((host_ip, port))
print(f"Init succesuful")

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  
if not cap.isOpened():
    print("Camera not found!")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        encoded, buffer = cv2.imencode('.jpg', frame)
        data = pickle.dumps(buffer)
        server_socket.sendto(data, ('192.168.0.154', port))
except Exception as e:
    print(f"Error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    server_socket.close()

# import cv2

# # Open the first connected camera (index 0)
# cap = cv2.VideoCapture(0)

# # Check if the camera opened successfully
# if not cap.isOpened():
#     print("Error: Could not open camera.")
# else:
#     print("Camera opened successfully!")