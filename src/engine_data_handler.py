import paho.mqtt.client as mqtt
import struct

class EngineDataHandler():


    def __init__(self, broker_address="localhost", topic=[("controller_enginee_data", 0), ("max_speed_data", 0)], publish_topic='enginee_velocity', max_velocity_topic="max_velocity_data"):
        self.client = mqtt.Client("EngineDataHandler")
        try:
            self.client.connect(broker_address)
        except Exception as e:
            print(f"Error connecting to broker at {broker_address}: {e}")
        self.topic = topic
        self.publish_topic = publish_topic
        self.max_velocity_value = 100
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        self.max_velocity_topic = max_velocity_topic
        print("Init successful engine_data_handler")

    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_forever()


    def send_max_velocity(self):
        try:
            print(f"HERE engine_data handler send_max_velocity {self.max_velocity_value}")
            msg = struct.pack('i', int(self.max_velocity_value))
            self.client.publish(self.max_velocity_topic, msg)
        except Exception as e:
            print(f"TEST ISSUE Issue with sending speed: {e}")    


    def send_speed(self, v, d, break_command):
        try:
            vp = self.v_map(v)
            db = self.d_map(d)
            print(f"Send speed v {v} mapped to {vp} with max_velocity {self.max_velocity_value}")
            msg = struct.pack('i??', int(vp), db, break_command)
            self.client.publish(self.publish_topic, msg)
        except Exception as e:
            print(f"Issue with sending speed: {e}")

    def v_map(self, v):
        try:
            vp = v / 1.5 * self.max_velocity_value
            if vp > self.max_velocity_value:
                vp = self.max_velocity_value
            return vp
        except Exception as e:
            print(f"Error in v_map: {e}")


    def d_map(self, d):
        return d >= 45



    def listener_callback(self, client, userdata, msg):
        print("listener callback engine_data_handler")
        if msg.topic == "controller_enginee_data":
            print("eeeeee in if")
            try:
                print("get topic controller_enginee_data")
                unpacked_data = struct.unpack('ff?', msg.payload)
                v = unpacked_data[0]
                direction = unpacked_data[1]
                break_command = unpacked_data[2]
                print(f'Received: {unpacked_data}')
                self.send_speed(v, direction, break_command)
            except struct.error as e:
                print(f"Error unpacking message on topic controller_enginee_data payload: {e}")
        elif msg.topic == "max_speed_data":
            try:
                unpacked_data = struct.unpack('i', msg.payload)
                self.max_velocity_value = unpacked_data[0]
                self.send_max_velocity()
            except struct.error as e:
                print(f"Error unpacking message on topic max_speed_data payload: {e}")


def main(args=None):
    engine_data_handler = EngineDataHandler()
    engine_data_handler.start()
    engine_data_handler.client.loop_stop()


if __name__ == '__main__':
    main()
