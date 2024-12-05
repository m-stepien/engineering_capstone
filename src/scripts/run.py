import subprocess
import os
import sys

<<<<<<< Updated upstream
nodes = ["engine_subscriber.py", "engine_data_handler.py", "servo_subscriber.py", "servo_data_handler.py", "main_publisher.py"]
path = ""
=======
nodes = ["engine_subscriber.py", "engine_data_handler.py", "servo_subscriber.py", "servo_data_handler.py", "main_publisher.py", "camera.py"]
path = "./../"
>>>>>>> Stashed changes
processes = []
for node in nodes:
    process = subprocess.Popen(["python3", path+node])
    processes.append(process)

for process in processes:
    process.wait()
