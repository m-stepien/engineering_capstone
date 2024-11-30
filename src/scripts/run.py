import subprocess
import os
import sys

nodes = ["main_publisher.py", "came_mock.py"]
path = ""
processes = []
for node in nodes:
    process = subprocess.Popen(["python3", path+node])
    processes.append(process)

for process in processes:
    process.wait()
