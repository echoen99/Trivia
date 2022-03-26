import socket
import select

HOST = "0.0.0.0"
PORT = 5678
MAX_MSG_LENGTH = 1024
SERVER_ADDRESS = (HOST, PORT)

def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen()
    print("Server is up and running, listening for clients...")
    client_sockets = []
    messages_to_send = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print(f"New data from client: {current_socket.getpeername()}")
                try:
                    data = current_socket.recv(MAX_MSG_LENGTH).decode()
                except:
                    print("Client connection lost")
                    data = "quit"

                if data.lower()=="quit":
                    print("Connection closed")
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    print(f"Client sent: {data}")
                    data_to_sent = f"{data.upper()}"
                    messages_to_send.append((current_socket, data_to_sent))

        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(message)
    
    server_socket.close()

main()