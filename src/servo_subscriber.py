import paho.mqtt.client as mqtt
from serwo import Servo
import struct


class ServoSubscriber():
    
    def __init__(self, broker_address="localhost", topic="servo_angle"):
        self.client = mqtt.Client("ServoSubscriber")
        try:
            self.client.connect(broker_address)
        except Exception as e:
            print(f"Issue with connection to the broker: {e}")

        self.topic = topic
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        self.servo = Servo()
        print("Init successful servo subscriber")

        
    def listener_callback(self, client, userdata, msg):
        try:
            angle = struct.unpack('i', msg.payload)[0]
            self.servo.start_go_to(angle)
            print("ServoSubscrivber")
            print(f"Received: {angle}")
        except Exception as e:
            print(f"something wrong with moving servo: {e}")

    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_forever()   

def main(args=None):
    servo_subscriber = ServoSubscriber()
    servo_subscriber.start()
    servo_subscriber.client.loop_stop()

if __name__ == '__main__':
    main()