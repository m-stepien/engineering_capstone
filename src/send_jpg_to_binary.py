import paho.mqtt.client as mqtt
import time

broker = "localhost" 
topic = "camera_data" 
image_path = "./frame.jpg"  

def publish_image(image_path, broker, topic):
    client = mqtt.Client()
    client.connect(broker)
    
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read() 
    try:
        while True:
            client.publish(topic, payload=binary_data, qos=1)
            print(f"Zdjęcie zostało wysłane jako dane binarne do topicu '{topic}'.")
            time.sleep(7)  
    except KeyboardInterrupt:
        print("Zatrzymano publikowanie.")
        client.disconnect()

publish_image(image_path, broker, topic)