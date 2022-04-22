##############################################################################
# server.py
##############################################################################

import select
import sys
from socket import socket, AF_INET, SOCK_STREAM

sys.path.append(".")
from u1.chatlib_skeleton import *
# To use chatlib functions or consts, use chatlib.****

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

# HELPER SOCKET METHODS
def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

def print_connected_users():
    global logged_users
    for u in logged_users:
        print("\t", u)

def build_and_send_message(conn: socket, code: str, data: str = ""):
    # copy from client
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    full_msg = build_message(code, data)
    conn.send(full_msg.encode())
    print("[SERVER] ", full_msg)	  # Debug print


def recv_message_and_parse(conn: socket):
    # copy from client
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    full_msg = conn.recv(MAX_MSG_LENGTH).decode()
    print("[CLIENT] ", full_msg)	  # Debug print
    cmd, data = parse_message(full_msg)
    return cmd, data


def build_send_recv_parse(conn: socket, code: str, data: str) -> tuple[str, str]:
    """Build & Send Message, then Recieve Message & Parse
    by calling: build_and_send_message
    and then: recv_message_and_parse
    :param socket conn: open connection
    :param str code: message code
    :param str data: message data
    :return tuple[str, str]: returns the response message code & data
    """
    build_and_send_message(conn, code, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"], "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
        "test":	{"password": "test", "score": 0, "questions_asked": []},
        "yossi":	{"password": "123", "score": 50, "questions_asked": []},
        "master":	{"password": "master", "score": 200, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket() -> socket:
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    # Implement code ...
    address = (SERVER_IP, SERVER_PORT)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen()
    return sock


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    # Implement code ...
    build_and_send_message(conn, PROTOCOL_SERVER["server_error"], error_msg)


# MESSAGE HANDLING


def handle_getscore_message(conn: socket, username: str):
    global users
    # Implement this in later chapters
    user_details = users.get(username)
    if not user_details:
        send_error(conn, f"Invalid username: {username}")
        return

    score = str(user_details["score"])
    build_and_send_message(conn, PROTOCOL_SERVER["your_score_msg"], score)


def handle_highscore_message(conn: socket):
    global users
    # Implement this in later chapters
    scores = []
    for user_details in sorted(users, key=lambda x: x["score"], reverse=True):
        username = user_details["username"]
        user_score = user_details["score"]
        scores.append(f"{username}: {user_score}")

    build_and_send_message(conn, PROTOCOL_SERVER["your_score_msg"], '/n'.join(scores))


def handle_logout_message(conn: socket):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users

    # Implement code ...
    logged_users.pop(conn.getpeername())
    conn.close()


def handle_login_message(conn: socket, data: str):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later

    # Implement code ...
    credentials = data.split("#")
    user = credentials[0]
    password = credentials[1]
    user_details = users.get(user)
    if not user_details:
        send_error(conn, f"Invalid username or password: {user}")
        return

    if user_details["password"] != password:
        send_error(conn, f"Invalid username or password: {password}")
        return

    build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"])
    address = conn.getpeername()
    # logged_user = (user, address)
    logged_users[address] = user


def handle_client_message(client_sockets, conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later

    # Implement code ...
    if cmd == PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)
        #print_connected_users()
    
    elif cmd == PROTOCOL_CLIENT["logout_msg"]:
        client_sockets.remove(conn)
        handle_logout_message(conn)
        #print_connected_users()
    
    elif cmd == PROTOCOL_CLIENT["my_score_msg"]:
        user = logged_users[conn.getpeername()]
        handle_getscore_message(conn, user)
    
    elif cmd == PROTOCOL_CLIENT["highscore_msg"]:
        handle_highscore_message(conn)
    
    else:
        send_error(conn, f"Invalid command: {cmd}")
        raise ValueError(f"Invalud command: {cmd}")


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")

    # Implement code ...
    print("Initilaizing databases...")
    users = load_user_database()
    questions = load_questions()

    print("Setting up server...")
    server_socket = setup_socket()
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
                    cmd, data = recv_message_and_parse(current_socket)
                    handle_client_message(client_sockets, current_socket, cmd, data)
                except:
                    print("Client connection lost")
                    client_sockets.remove(current_socket)
                    handle_logout_message(current_socket)


if __name__ == '__main__':
    main()
