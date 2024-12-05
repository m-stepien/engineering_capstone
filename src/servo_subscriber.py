import paho.mqtt.client as mqtt
from serwo import Servo
import struct


class ServoSubscriber():
    
    def __init__(self, broker_address="localhost", topic="servo_angle"):
        self.client = mqtt.Client("ServoSubscriber")
        self.client.connect(broker_address)
        self.topic = topic
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        self.servo = Servo()
        print("Init successful")

        
    def listener_callback(self, client, userdata, msg):
        angle = struct.unpack('i', msg.payload)[0]
        self.servo.move(angle)
        print("ServoSubscrivber")
        print(f"Received: {angle}") 

    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_forever()   

def main(args=None):
    servo_subscriber = ServoSubscriber()
    servo_subscriber.start()
    servo_subscriber.client.loop_stop()

if __name__ == '__main__':
    main()