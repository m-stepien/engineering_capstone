import base64
import socket
import threading
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


def receive_messages(sock, cipher):
    """
    Function to continuously receive messages from the server.
    """
    try:
        while True:
            encrypted_data = sock.recv(1024)
            decoded_data = base64.b64decode(encrypted_data)
            decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
            message = decrypted_data.decode('utf-8')
            print(f"\n[Server]: {message}")
    except Exception as e:
        print(f"Error in receiving messages: {e}")
    finally:
        sock.close()


def send_messages(sock, cipher):
    try:
        while True:
            command = input("Enter command to send to the server: ")
            if command.lower() == 'disconnect':
                print("Disconnecting from server...")
                break

            ciphered_data = cipher.encrypt(pad(command.encode('utf-8'), AES.block_size))
            sock.send(ciphered_data)
    except Exception as e:
        print(f"Error in sending messages: {e}")
    finally:
        sock.close()


receive_thread = threading.Thread(target=receive_messages, args=(client_socket, cipher))
send_thread = threading.Thread(target=send_messages, args=(client_socket, cipher))

receive_thread.start()
send_thread.start()

send_thread.join()
receive_thread.join()

print("Client socket closed.")
