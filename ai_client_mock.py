import paho.mqtt.client as mqtt

frame_counter = 0
def on_message(client, userdata, message):
    global frame_counter
    try:
        buffer = message.payload

        filename = f"./test/frame_{frame_counter}.jpg"
        frame_counter += 1

        with open(filename, "wb") as f:
            f.write(buffer)

        print(f"Frame saved as '{filename}'")
    except Exception as e:
        print(f"Error saving frame: {e}")

client = mqtt.Client("ClientSaver")
client.on_message = on_message
client.connect("localhost") 
client.subscribe("camera_data")
client.loop_forever()