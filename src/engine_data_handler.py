import paho.mqtt.client as mqtt

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
        self.client.loop_forever()

    def send_speed(self, v):
        speed_msg = UInt8()
        speed_msg.data = v_map(v)

    def v_map(self, v):
        #will be implemented if needed when creating connection to mobile app
        return v
    
    def listener_callback(self, msg):
        print(f'Received: {msg}')


def main(args=None):
    engine_data_handler = EngineDataHandler()
    engine_data_handler.start()
    engine_data_handler.client.loop_stop()

if __name__ == '__main__':
    main()