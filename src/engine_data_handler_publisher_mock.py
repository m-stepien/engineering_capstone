import time
import struct
import paho.mqtt.client as mqtt

def send_velocity():
    broker_address = "localhost" 
    topic = "max_velocity_data"
    
    client = mqtt.Client()
    client.connect(broker_address)
    i = 0
    try:
        while True:
            if i%3==0:
                velocity = 100
            elif i%3==1:
                velocity = 80
            elif i%3==2:
                velocity = 70
            msg = struct.pack('i', int(velocity))
            client.publish(topic, msg)
            print(f"Wysłano maksymalna prędkość: {velocity}")
            time.sleep(3)  
            i+=1
    except KeyboardInterrupt:
        print("Zatrzymano publikowanie.")
        client.disconnect()

if __name__ == "__main__":
    send_velocity()