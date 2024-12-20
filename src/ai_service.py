import paho.mqtt.client as mqtt
import struct


class AiService():
    def __init__(self, broker_address="localhost", topic="camera_data", publish_topic="max_speed_data"):
        self.client = mqtt.Client("AiNode")
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
        print("Init successful Ai Service")
        self.i = 0

    def listener_callback(self, client, userdata, msg):
        try:
            print("AI service recive image from camera")
            buffer = msg.payload
            result = self.evaluate_image(buffer)
            if result is not None:
                self.publish_max_speed_data(int(result))
        except Exception as e:
            print(f"Issue with image: {e}")
            return 0
        

        
        
    def publish_max_speed_data(self, data):
        msg = struct.pack('i', int(data))
        self.client.publish(self.publish_topic, msg)
        print(f'Sending max speed data: {data}')

    def evaluate_image(self, buffer):
        self.i+=1
        if self.i % 3 == 0:
            return 80
        elif self.i % 3 == 1:
            return 70
        else:
            return 100
#        return 80
    
    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_forever()   


def main():
    ai_service = AiService()
    ai_service.start()
    ai_service.client.loop_stop()

if __name__ == '__main__':
    main()