from motor import MotorMock
import paho.mqtt.client as mqtt


class EngineSubscriber():
    
    def __init__(self, broker_address='localhost', topic='enginee_velocity'):
        self.client = mqtt.Client("EngineSubscriber")
        self.client.connect(broker_address)
        self.topic = topic
        self.client.subscribe(self.topic)
        self.client.on_message = self.listener_callback
        self.motor = MotorMock()
        self.motor_controler = MotorMock()
        print("Init successful")

    
    def listener_callback(self, msg):
        velocity = int(msg.payload.decode())
        self.motor.move_forward(velocity)
        print(f'Received: {velocity}')

    
    def start(self):
        print(f"Subscribing to topic: {self.topic}")
        self.client.loop_start()   



def main(args=None):
    enginee_subscriber = EngineSubscriber()
    enginee_subscriber.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down.")
        enginee_subscriber.client.loop_stop()

if __name__ == '__main__':
    main()