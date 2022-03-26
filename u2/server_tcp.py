import random
import socket
import time
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5678
MAX_MSG_LENGTH = 1024
SERVER_ADDRESS = (HOST, PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen()
print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")

while True:
    data = client_socket.recv(MAX_MSG_LENGTH).decode()
    print(f"Client sent: {data}")
    if data == "Quit":
        print("Closing client socket now...")
        client_socket.send("Bye".encode())
        break
    elif data == "Bye":
        data_to_sent = " "
    elif data == "NAME":
        data_to_sent = "Server 4 u :)"
    elif data == "TIME":
        data_to_sent = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elif data == "RAND":
        data_to_sent = str(random.randint(1,10))
    else:
        data_to_sent = f"{data.upper()}!!!"

    client_socket.send(data_to_sent.encode())


client_socket.close()
server_socket.close()   
