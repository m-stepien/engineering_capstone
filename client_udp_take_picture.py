import os
import cv2
import socket
import pickle
import numpy as np  
import time

output_folder = "./dataset/100"
os.makedirs(output_folder, exist_ok=True)



def client_communication():
    host = 'inz.local' 
    host_ip = 'inz.local' 
    port = 12345    
    port2 = 12346
    i = 11

    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket2.connect((host, port))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
    

    client_socket.bind(('', port2)) 
    print(f"Client ready to receive video from {host_ip}:{port2}")
    time.sleep(6)
    try:
        while True:
            data, addr = client_socket.recvfrom(65536)
            frame = np.frombuffer(data, dtype=np.uint8)
            image = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            if image is not None:
                cv2.imshow("Video", image)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                elif key == 13:
                    filename = os.path.join(output_folder, f"frame_{i}.jpg")
                    cv2.imwrite(filename, image)
                    print(f"Frame saved: {filename}")
                    i+=1
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()
        client_socket.close()


if __name__ == '__main__':
    client_communication()

