import subprocess
import os
import sys
#delete mock after when writting frontend comunication of current speed end
#"engine_subscriber_mock.py", "send_jpg_to_binary.py"
nodes = ["engine_subscriber.py", "engine_data_handler.py", "servo_subscriber.py", "servo_data_handler.py", "ai_service.py", "main_publisher.py", "camera.py"]

path = ""
processes = []
for node in nodes:
    process = subprocess.Popen(["python3", path+node])
    processes.append(process)

for process in processes:
    process.wait()
