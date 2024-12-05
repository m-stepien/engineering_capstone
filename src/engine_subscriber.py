from motor import Motor
import paho.mqtt.client as mqtt
import struct

class EngineSubscriber():
    
    def __init__(self, broker_address='localhost', topic='enginee_velocity'):
        self.client = mqtt.Client("EngineSubscriber")

        try:
            self.client.connect(broker_address)
        except Exception as e:
            print(f"Problem with connection to broker: {e}")

        self.topic = topic
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        self.motor = Motor()
        print("Init successful")

    
    def listener_callback(self, client, userdata, msg):
        try:
            unpacked_data = struct.unpack('i?', msg.payload)
        except Exception as e:
            print(f"Issue with unpacking struct: {e}")
            return 0

        v = unpacked_data[0]
        d = unpacked_data[1]
        if d:
            self.motor.move_forward(v)
        else:
            self.motor.move_backward(v)    
        print(f'Received: {v}')

    
    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_forever()   



def main(args=None):
    enginee_subscriber = EngineSubscriber()
    enginee_subscriber.start()
    enginee_subscriber.client.loop_stop()

if __name__ == '__main__':
    main()