import cv2
import socket
import pickle
import struct
import os
import glob
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_ip = '0.0.0.0'  
port = 12346
server_socket.bind((host_ip, port))
print(f"Init succesuful")
mock_images_path = "frames/*.jpg"  
mock_images = [cv2.imread(img_path) for img_path in sorted(glob.glob(mock_images_path))]
# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  

try:
    while True:
        for frame in mock_images:
            if frame is None:
                print("Failed to load mock frame.")
                continue
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            data = pickle.dumps(buffer)
            server_socket.sendto(buffer.tobytes(), ('192.168.0.73', port))

except Exception as e:
    print(f"Error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    server_socket.close()
