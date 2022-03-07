from base64 import encode
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 8820
address = (HOST, PORT)
my_socket.connect(address)

data = "" 
while data != "Bye":
    msg = input("Please enter your message\n")
    my_socket.send(msg.encode())
    data = my_socket.recv(1024).decode()
    print(f"The server sent data:{data}")

my_socket.close()
