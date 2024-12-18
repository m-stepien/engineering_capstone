import base64
import socket
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

salt = b'\xda\x02\xd9A\xcd\x19\xd9U]x\xe10\xc1\xb5\x92\xbd\x0e\x8eA\x89\xafM\xf9KDf\x96\xb0\xfa+E\xb6'
password = "veryStrongPassword"

key = PBKDF2(password, salt, dkLen=32)
iv = b'\xda8^(/\x16\xd7\xd0\x94\xc4\xa8}n\x11\xee\xa1'

cipher = AES.new(key, AES.MODE_CBC, iv=iv)

# inz.local
server_address = ('inz.local', 12345)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)
print(f"Connected to server at {server_address}")


def receive_message(sock, cipher):
    try:
        encrypted_data = sock.recv(1024)
        if not encrypted_data:
            return None
        
        decoded_data = base64.b64decode(encrypted_data)
        
        decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
        
        message = decrypted_data.decode('utf-8')
        return message
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None


try:
    while True:
        command = input("Enter command to send to the server: ")

        ciphered_data = cipher.encrypt(pad(command.encode('utf-8'), AES.block_size))
        client_socket.send(ciphered_data)
        print(f"Sent command: {ciphered_data}")

        if command.lower() == 'disconnect':
            break

        response = receive_message(client_socket, cipher)
        if response is not None:
            print(f"Received response: {response}")
        else:
            print("No response received or connection closed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
    print("Client socket closed.")