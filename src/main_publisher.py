import socket
import json
import threading
import struct
import paho.mqtt.client as mqtt


class MainPublisher(): 

    def __init__(self, broker_address="localhost"):
        self.client = mqtt.Client("MainPublisher")

        try:
            self.client.connect(broker_address)
        except Exception as e:
            print(f"Issue with connection to broker: {e}")

        self.topic_publish_enginee = 'controller_enginee_data'
        self.topic_publish_servo = 'controller_turn_data'

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', 12345))
            self.server_socket.listen(1)
            self.client_socket = None
            print("init succesfull")
            self.accept_connection()
        except Exception as e:
            print(f"Issue during server socker creation: {e}")

    def start_socket(self, client_socket):
        try:
            while client_socket:
                data = client_socket.recv(1024)
                if data:
                    json_data = json.loads(data.decode('utf-8'))
                    print(f"Received command: {json_data}")
                    try:
                        angle = self.parse_degree(json_data)
                        self.publish_turn_message(angle)
                        enginee_data = self.parse_velocity(json_data)
                        self.publish_velocity_message(enginee_data)
                        self.client_socket.send("ok".encode('utf-8'))
                    except Exception as e:
                        print(f"something wrong with received message: {e}")
                        self.client_socket.send("Something is wrong check the command".encode('utf-8'))


                else:
                    print("Client disconnected unexpectedly.")
                    client_socket.close()
                    self.client_socket = None
                    break
        except Exception as e:
            print(f"Error receiving command: {e}")
            self.client_socket.close()
           

    def accept_connection(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection established with {addr}")
            self.client_socket = client_socket
            client_thread = threading.Thread(target=self.start_socket, args=(client_socket,))
            client_thread.start()

    

    def destroy_node(self):
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
        super().destroy_node()


    def publish_velocity_message(self, data):
        print("IMPORTANT")
        msg = struct.pack('ff', float(data[0]), float(data[1]))
        self.client.publish(self.topic_publish_enginee, msg) 
        print('Sending move engine data: "%s"' % data)

    
    def publish_turn_message(self, angle_degree):
        msg = struct.pack('f', float(angle_degree))
        self.client.publish(self.topic_publish_servo, msg)
        print('Sending turn engine data: "%s"' % msg)



    def parse_degree(self, json_data):
        return json_data.get("angle", {}).get("degree")
    

    def parse_velocity(self, json_data):
        data = []
        data.append(json_data.get("force"))
        data.append(json_data.get("position", {}).get("y"))
        return data
    

def main(args=None):
    main_publisher = MainPublisher()
    main_publisher.client.loop_start()
    main_publisher.start_socket()

# def main(args=None):
#     main_publisher = MainPublisher()
#     main_publisher.start_socket()
#     main_publisher.client.loop_stop()

if __name__ == '__main__':
    main()