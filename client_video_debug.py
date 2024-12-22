import cv2
import socket
import pickle
import numpy as np  
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import threading
import time


key = b'\xde?\xb0*/\x1d\xb0\xf5\xad\xf4\xa63\xf5\x0c\xbc\xb2)\xe1\x9b\x08n\x93\xdaxm\x1d\x9f\x84Z\xe8\xf6#'
iv = b'\xda8^(/\x16\xd7\xd0\x94\xc4\xa8}n\x11\xee\xa1'
cipher = AES.new(key, AES.MODE_CBC, iv=iv)


def encrypt_message(data):
    json_data = json.dumps(data).encode('utf-8')
    padded_data = pad(json_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encoded_data = base64.b64encode(encrypted_data)
    return encoded_data

def decrypt_message(data):
    encrypted_data = base64.b64decode(data)
    cipher_decrypt = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher_decrypt.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')

def send_message(client_socket, command_data):
    try:
        encrypted_message = encrypt_message(command_data)
        client_socket.send(encrypted_message)
        print(f"Wysłano zaszyfrowane dane: {command_data}")
    except Exception as e:
        print(f"Błąd podczas wysyłania wiadomości: {e}")

def receive_messages(client_socket):
    try:
        while True:
            response = client_socket.recv(2048)
            if response:
                try:
                    decrypted_response = decrypt_message(response)
                    print(f"Otrzymano odpowiedź od serwera: {decrypted_response}")
                except Exception as e:
                    print(f"Błąd przy dekodowaniu odpowiedzi: {e}")
            else:
                print("Serwer zamknął połączenie.")
                break
    except Exception as e:
        print(f"Błąd podczas odbierania wiadomości: {e}")
    finally:
        client_socket.close()
def client_communication():
    host = 'inz.local'  
    port = 12345        
    command_data = {
        "type": "move",
        "angle": {"degree": 90.0},
        "force": 1.5,
        "position": {"x": 0.0, "y": 50}
    }

    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket2.connect((host, port))
    receiver_thread = threading.Thread(target=receive_messages, args=(client_socket2,))
    receiver_thread.daemon = True
    receiver_thread.start()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
    host_ip = 'inz.local'
    port = 12346

    client_socket.bind(('', port)) 
    print(f"Client ready to receive video from {host_ip}:{port}")
    time.sleep(6)
    try:
        while True:
            data, addr = client_socket.recvfrom(65536)
            frame = np.frombuffer(data, dtype=np.uint8)
            image = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            if image is not None:
                cv2.imshow("Video", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            send_message(client_socket2, command_data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()
        client_socket.close()


if __name__ == '__main__':
    client_communication()

