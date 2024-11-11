import socket

server_address = ('localhost', 12345) 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)
print(f"Connected to server at {server_address}")

try:
    while True:
        command = input("Enter command to send to the server (type 'disconnect' to disconnect): ")
        
        client_socket.send(command.encode('utf-8'))
        print(f"Sent command: {command}")

        if command.lower() == 'disconnect':
            break  # Exit the loop to close the connection

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received response: {response}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
    print("Client socket closed.")
