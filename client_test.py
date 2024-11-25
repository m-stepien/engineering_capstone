import socket
import time

server_address = ("inz.local", 12345) 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)
print(f"Connected to server at {server_address}")

try:
    for _ in range(0, 100):
        time.sleep(0.1)
        command = '{"angle": {"degree": 90.791146,"radian": 1.5846044},"force": 1.9891304,"position":{"x": 39.17154,"y": 99.9942801},"type": "move"}'
        
        client_socket.send(command.encode('utf-8'))
        print(f"Sent command: {command}")

       
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received response: {response}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
    print("Client socket closed.")
