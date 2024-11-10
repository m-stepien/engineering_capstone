import socket
import json
import paho.mqtt.client as mqtt


#todo done check is angle send succesful to servo_data_handler 
#todo done implement serwo class
#todo done servo_data_handler
#todo implement serwo mock
#todo done solve sudo privilage required
#todo done add github to simpler pushing project progression
class MainPublisher(): 

    def __init__(self, broker_address="localhost"):
        self.client = mqtt.Client("MainPublisher")
        self.client.connect(broker_address)
        self.topic_publish_enginee = 'controller_enginee_data'
        self.topic_publish_servo = 'controller_turn_data'
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 12345))
        self.server_socket.listen(1)
        self.client_socket = None
        self.accept_connection()
        print("init succesfull")


    def start_socket(self):
        try:
            while self.client_socket:
                data = self.client_socket.recv(1024)
                if data:
                    json_data = json.loads(data.decode('utf-8'))
                       # self.get_logger().info(f"Received command: {json_data}")
                    angle = self.parse_degree(json_data)
                    self.publish_turn_message(angle)
                    self.client_socket.send("ok".encode('utf-8'))
                        # enginee_data = self.parse_velocity(json_data)   
                        # self.publish_velocity_message(enginee_data)
                else:
                      #  self.get_logger().info("Client disconnected unexpectedly.")
                    self.client_socket.close()
                    self.client_socket = None
        except Exception as e:
            print(f"Error receiving command: {e}")
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None


    def accept_connection(self):
        self.client_socket, addr = self.server_socket.accept()
     #   self.get_logger().info(f"Connection established with {addr}")
    

    def destroy_node(self):
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
        super().destroy_node()


    def publish_velocity_message(self, data):
        msg = int(data)
        #self.get_logger().info('Sending move engine data: "%s"' % msg.data)
        self.client.publish(self.topic_publish_enginee, msg) 


    def publish_turn_message(self, angle_degree):
        msg = float(angle_degree)
       # self.get_logger().info('Sending turn engine data: "%s"' % msg.data)
        self.client.publish(self.topic_publish_servo, msg)


    def parse_degree(self, json_data):
        return json_data.get("angle", {}).get("degree")
    

    def parse_velocity(self, json_data):
        data = []
        data.append(json_data.get("force"))
        data.append(json_data.get("position", {}).get("y"))
        return data
    

def main(args=None):
    main_publisher = MainPublisher()
    main_publisher.start_socket()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down.")
        main_publisher.client.loop_stop()

if __name__ == '__main__':
    main()
