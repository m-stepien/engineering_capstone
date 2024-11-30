import paho.mqtt.client as mqtt
import struct
from motor import Motor


class EngineDataHandler():

    def __init__(self, broker_address="localhost", topic="controller_enginee_data", publish_topic='enginee_velocity'):
        self.client = mqtt.Client("EngineDataHandler")

        try:
            self.client.connect(broker_address)
        except Exception as e:
            print(f"Error connecting to broker at {broker_address}: {e}")

        self.topic = topic
        self.publish_topic = publish_topic

        try:
            self.client.subscribe(self.topic)
        except Exception as e:
            print(f"Error subscribing to topic {self.topic}: {e}")

        self.client.on_message = self.listener_callback
        print("Init successful")

    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_forever()

    def send_speed(self, v, d):
        try:
            vp = self.v_map(v)
            db = self.d_map(d)
            msg = struct.pack('i?', int(vp), db)
            self.client.publish(self.publish_topic, msg)
        except Exception as e:
            print(f"Issue with sending speed: {e}")

    def v_map(self, v):
        try:
            vp = v / 1.5 * 100
            if vp > 100:
                vp = 100
            return vp
        except Exception as e:
            print(f"Error in v_map: {e}")

    def d_map(self, d):
        return d > 0

    def listener_callback(self, client, userdata, msg):
        try:
            unpacked_data = struct.unpack('ff', msg.payload)
            v = unpacked_data[0]
            direction = unpacked_data[1]
            print(f'Received: {unpacked_data}')
            self.send_speed(v, direction)
        except struct.error as e:
            print(f"Error unpacking message payload: {e}")


def main(args=None):
    engine_data_handler = EngineDataHandler()
    engine_data_handler.start()
    engine_data_handler.client.loop_stop()


if __name__ == '__main__':
    main()
