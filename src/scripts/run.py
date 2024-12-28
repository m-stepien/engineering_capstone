import subprocess
import time
nodes = ["engine_subscriber.py", "engine_data_handler.py", "servo_subscriber.py", "servo_data_handler.py", "ai_service.py", "main_publisher.py", "camera.py"]
# /home/bilbo/capstone/src/
path = ""
processes = []
for node in nodes:
    process = subprocess.Popen(["python3", path+node])
    processes.append(process)

for process in processes:
    process.wait()
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    for process in processes:
        process.terminate()