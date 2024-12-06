import socket
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

salt = b'\xda\x02\xd9A\xcd\x19\xd9U]x\xe10\xc1\xb5\x92\xbd\x0e\x8eA\x89\xafM\xf9KDf\x96\xb0\xfa+E\xb6'
password = "veryStrongPassword"

key = PBKDF2(password, salt, dkLen=32)
iv = b'\xda8^(/\x16\xd7\xd0\x94\xc4\xa8}n\x11\xee\xa1'

cipher = AES.new(key, AES.MODE_CBC, iv=iv)

#inz.local
server_address = ('localhost', 12345) 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)
print(f"Connected to server at {server_address}")

try:
    while True:
        command = input("Enter command to send to the server")

        ciphered_data = cipher.encrypt(pad(command.encode('utf-8'), AES.block_size))

        client_socket.send(ciphered_data)
        print(f"Sent command: {ciphered_data}")

        if command.lower() == 'disconnect':
            break

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received response: {response}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
    print("Client socket closed.")
