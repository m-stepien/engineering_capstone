import socket
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import threading
import time

# Klucz i wektor inicjalizacyjny (te same co na serwerze)
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
    host = 'localhost'  
    port = 12345        
    command_data = {
        "type": "move",
        "angle": {"degree": 45.0},
        "force": 1.5,
        "position": {"x": 0.0, "y": 0.5}
    }

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Połączono z serwerem.")

        receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receiver_thread.daemon = True
        receiver_thread.start()

        send_message(client_socket, command_data)

        while True:
            send_message(client_socket, command_data)
            time.sleep(0.1)

    except Exception as e:
        print(f"Błąd komunikacji: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    client_communication()
