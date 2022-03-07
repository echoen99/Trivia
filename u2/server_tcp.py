import socket

HOST = "0.0.0.0"
PORT = 8820
SERVER_ADDRESS = (HOST, PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen()
print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")

while True:
    data = client_socket.recv(1024).decode()
    print(f"Client sent: {data}")
    if data == "Quit":
        print("Closing client socket now...")
        client_socket.send("Bye".encode())
        break
    elif data == "Bye":
        data = " "

    client_socket.send(data.encode())

client_socket.close()
server_socket.close()   
