import paho.mqtt.client as mqtt
import struct



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
        if a<180:
            mapped = a - 90
        elif a<270:
            mapped = 180 - (a-180)-90
        else:
            mapped = -90+360-a
        return int(mapped)


    def send_angle(self, a):
        a=self.angle_map(a)
        print(f'Map to: {a}')
        msg=struct.pack('i', int(a))
        self.client.publish(self.publish_topic, msg)
    

    def listener_callback(self, client, userdata, msg):
        angle = struct.unpack('f', msg.payload)[0]
        print(f'Received: {angle}')
        self.send_angle(angle)

    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_start()   


def main(args=None):
    servo_data_handler = ServoDataHandler()
    servo_data_handler.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down.")
        servo_data_handler.client.loop_stop()

if __name__ == '__main__':
    main()