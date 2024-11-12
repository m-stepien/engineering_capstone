import paho.mqtt.client as mqtt


class ServoDataHandler():
    
    def __init__(self, broker_address="localhost", topic="controller_turn_data", publish_topic='servo_angle'):
        self.client = mqtt.Client("ServoDataHandler")
        self.client.connect(broker_address)
        self.topic = topic
        self.publish_topic=publish_topic
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        print("Init successful")

    
    def angle_map(self, a):
        mapped = a - 90
        return int(mapped)


    def send_angle(self, a):
        a=self.angle_map(a)
        print(f'Map to: {angle_msg.data}')
        self.client.publish(self.publish_topic, message)
    

    def listener_callback(self, msg):
        message = msg.payload.decode()
        print(f'Received: {message}')
        self.send_angle(message)

    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_forever()   


def main(args=None):
    servo_data_handler = ServoDataHandler()
    servo_data_handler.start()


if __name__ == '__main__':
    main()