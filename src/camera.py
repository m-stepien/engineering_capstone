import cv2
import socket
import pickle
import struct
import time
import paho.mqtt.client as mqtt
# '192.168.0.124'
class Camera():
    def __init__(self, broker_address="localhost", topic="client_ip_data", frame_to_send_number=160):
        self.client = mqtt.Client("Camera")
        self.frame_counter = 0
        self.frame_to_send_number = frame_to_send_number
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host_ip = '0.0.0.0'  
        self.port = 12346
        self.server_socket.bind((self.host_ip, self.port))
        self.client.connect(broker_address)
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  
        self.fps = 30
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) #640
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) #480
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.frame_duration = 1 / self.fps
        self.topic_publish_camera = 'camera_data'
        self.client_ip = None
        self.topic = topic
        self.client.on_message = self.listener_callback
        self.client.subscribe(self.topic, qos=2)
        if not self.cap.isOpened():
            print("Error: Camera not initialized!")
            self.cap.release()
            self.server_socket.close()
            exit()
        print(f"Init succesuful camera")


    def start_camera(self):
        try:
            self.wait_for_client_ip()
            print(f"outsite wait with {self.client_ip}")
            last_frame_time = time.perf_counter()
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                self.server_socket.sendto(buffer, (self.client_ip, self.port))
                elapsed_time = time.perf_counter() - last_frame_time
                if elapsed_time < self.frame_duration:
                    time.sleep(self.frame_duration - elapsed_time)
                self.frame_counter +=1
                if self.frame_counter == self.frame_to_send_number:
                    self.publish_camera_message(buffer)
                    self.frame_counter = 0
                last_frame_time = time.perf_counter()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            self.server_socket.close()
    
    
    def publish_camera_message(self, data):
        self.client.publish(self.topic_publish_camera, data.tobytes()) 
        print('Sending camera frame: "%s"' % data)
    

    def listener_callback(self, client, userdata, msg):
        self.client_ip = msg.payload.decode()
        print(f"Camera received client ip {self.client_ip}")


    def wait_for_client_ip(self):
        print("Camera waiting for client IP...")
        while self.client_ip is None:
            time.sleep(0.1) 

def main():
    camera = Camera(broker_address="localhost", frame_to_send_number=160)
    camera.client.loop_start() 
    try:
        camera.start_camera()
    except KeyboardInterrupt:
        print("Camera loop interrupted.")
    finally:
        camera.client.loop_stop() 
        print("Camera application stopped.")

if __name__ == '__main__':
    main()
