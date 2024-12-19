import time
import struct
import paho.mqtt.client as mqtt

def send_velocity():
    broker_address = "localhost" 
    topic = "current_velocity_data"
    
    client = mqtt.Client()
    client.connect(broker_address)
    
    try:
        while True:
            velocity = 50
            msg = struct.pack('i', int(velocity))
            client.publish(topic, msg)
            print(f"Wysłano prędkość: {velocity}")
            time.sleep(0.5)  
    except KeyboardInterrupt:
        print("Zatrzymano publikowanie.")
        client.disconnect()

if __name__ == "__main__":
    send_velocity()