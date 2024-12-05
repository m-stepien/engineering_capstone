import cv2
import socket
import pickle
import struct
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_ip = '0.0.0.0'  
port = 12346
server_socket.bind((host_ip, port))
print(f"Init succesuful")

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  
fps = 30
cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) #640
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) #480
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
frame_duration = 1 / fps 

if not cap.isOpened():
    print("Error: Camera not initialized!")
    cap.release()
    server_socket.close()
    exit()
try:
    last_frame_time = time.perf_counter()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        server_socket.sendto(buffer, ('192.168.0.124', port))
        elapsed_time = time.perf_counter() - last_frame_time
        if elapsed_time < frame_duration:
            time.sleep(frame_duration - elapsed_time)
        last_frame_time = time.perf_counter()
except Exception as e:
    print(f"Error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    server_socket.close()
