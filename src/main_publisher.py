import base64
import socket
import json
import threading
import struct
import paho.mqtt.client as mqtt
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

salt = b'\xda\x02\xd9A\xcd\x19\xd9U]x\xe10\xc1\xb5\x92\xbd\x0e\x8eA\x89\xafM\xf9KDf\x96\xb0\xfa+E\xb6'
password = "veryStrongPassword"
key = b'\xde?\xb0*/\x1d\xb0\xf5\xad\xf4\xa63\xf5\x0c\xbc\xb2)\xe1\x9b\x08n\x93\xdaxm\x1d\x9f\x84Z\xe8\xf6#'
iv = b'\xda8^(/\x16\xd7\xd0\x94\xc4\xa8}n\x11\xee\xa1'

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
# topic=[("current_velocity_data", 0), ("max_velocity_data", 0)]
class MainPublisher():

    def __init__(self, broker_address="localhost", topic="current_velocity_data"):
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
            self.curent_velocity_info = 0
            self.max_velocity_info = 100
            print("init succesfull main publisher")
            self.accept_connection()
        except Exception as e:
            print(f"Issue during server socker creation: {e}")
        self.topic = topic
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        


    def start_socket(self, client_socket):
        try:
            client_socket.settimeout(3)
            while client_socket:
                try:
                    data = client_socket.recv(2048)
                    if data:
                        encrypted_data = base64.b64decode(data)
                        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
                        start_index = decrypted_data.find(b'{')
                        json_data = decrypted_data[start_index:]
                        if start_index != -1:
                            json_data = json.loads(json_data.decode('utf-8'))
                            print(f"Received command: {json_data}")
                            command_type = self.get_command_type(json_data)
                            if command_type == "move":
                                try:
                                    angle = self.parse_degree(json_data)
                                    self.publish_turn_message(angle)
                                    enginee_data = self.parse_velocity(json_data)
                                    self.publish_velocity_message(enginee_data)
                                    self.client_socket.send("ok".encode('utf-8'))
                                except Exception as e:
                                    print(f"something wrong with received message: {e}")
                                    self.client_socket.send("Something is wrong check the command".encode('utf-8'))
                            elif command_type == "hold":
                                continue
                            elif command_type == "stop":
                                self.publish_velocity_message([0, 0, False])
                            elif command_type == "break":
                                self.publish_velocity_message([0, 0, True])
                            else:
                                print(f"There is no such command as {command_type}")
                                continue
                    else:
                        print("Client disconnected unexpectedly.")
                        client_socket.close()
                        client_socket = None
                        break
                except socket.timeout:
                    self.publish_velocity_message([0, 0, True])
                except Exception as e:
                    print(f"Error receiving command: {e}")
                    self.client_socket.send("Something is wrong check the command".encode('utf-8'))
                self.show_me_velocity()
            print(f"Engine turn off")
            self.publish_velocity_message([0, 0, True])
        except Exception as e:
            print(f"Socket issue :{e}")


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
        print("jestem w publish_velocity")
        msg = struct.pack('ff?', float(data[0]), float(data[1]), data[2])
        self.client.publish(self.topic_publish_enginee, msg)
        print('Sending move engine data: "%s"' % data)


    def publish_turn_message(self, angle_degree):
        msg = struct.pack('f', float(angle_degree))
        self.client.publish(self.topic_publish_servo, msg)
        print('Sending turn engine data: "%s"' % angle_degree)


    def parse_degree(self, json_data):
        return json_data.get("angle", {}).get("degree")

    
    def parse_velocity(self, json_data):
        data = []
        data.append(json_data.get("force"))
        data.append(json_data.get("position", {}).get("y"))
        command_type = self.get_command_type(json_data)
        data.append(command_type == "break")
        return data


    def get_command_type(self, command):
        command_type = command.get("type")
        return command_type
    

    def show_me_velocity(self):
        print(f"MAIN PUBLISHER CURRENT {self.curent_velocity_info}")
        print(f"MAIN PUBLISHER MAX {self.max_velocity_info}")


    def listener_callback(self, client, userdata, msg):
        try:
            unpacked_data = struct.unpack('i', msg.payload)
            print(f"HERE2 get velocity {unpacked_data[0]}")
            self.curent_velocity_info = unpacked_data[0]
        except struct.error as e:
            print(f"Error unpacking message on topic controller_enginee_data payload: {e}")
        # if msg.topic == "current_velocity_data":
        #     try:
        #         unpacked_data = struct.unpack('i', msg.payload)
        #         print(f"HERE2 get velocity {unpacked_data[0]}")
        #         self.curent_velocity_info = unpacked_data[0]
        #     except struct.error as e:
        #         print(f"Error unpacking message on topic controller_enginee_data payload: {e}")
        # elif msg.topic == "max_velocity_data":
        #     try:
        #         unpacked_data = struct.unpack('i', msg.payload)
        #         self.max_velocity_info = unpacked_data[0]
        #     except struct.error as e:
        #         print(f"Error unpacking message on topic max_speed_data payload: {e}")
        # else:
        #     print("ISSUE TEST im not even in if")




def main(args=None):
    main_publisher = MainPublisher()
    main_publisher.client.loop_start()
    main_publisher.start_socket()
    main_publisher.client.loop_stop()


if __name__ == '__main__':
    main()
