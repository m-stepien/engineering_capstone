import paho.mqtt.client as mqtt
import struct
from motor import Motor

class EngineDataHandler():
    
    def __init__(self, broker_address="localhost", topic="controller_enginee_data", publish_topic='enginee_velocity'):
        self.client = mqtt.Client("EngineDataHandler")
        self.client.connect(broker_address)
        self.topic = topic
        self.publish_topic=publish_topic
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        print("Init successful")


    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_start() 

    def send_speed(self, v, d):
        vp = self.v_map(v)
        db = self.d_map(d)
        msg=struct.pack('i?', int(vp), db)
        print("SENDING DATA")
        self.client.publish(self.publish_topic, msg)


    def v_map(self, v):
        vp = v/1.5 * 100
        if vp>100:
            vp=100
        return vp
    
    def d_map(self, d):
        return d>0
    
    def listener_callback(self, client, userdata, msg):
        unpacked_data = struct.unpack('ff', msg.payload)
        v = unpacked_data[0]
        direction = unpacked_data[1]
        print(f'Received: {msg}')
        print(f"V {v}")
        print(f"D {direction}")
        self.send_speed(v,direction)

def main(args=None):
    engine_data_handler = EngineDataHandler()
    engine_data_handler.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down.")
        engine_data_handler.client.loop_stop()

if __name__ == '__main__':
    main()