import sys
from typing import Tuple

sys.path.append(".")
from socket import AF_INET,SOCK_STREAM, socket
# To use chatlib functions or consts, use chatlib.****
from u1.chatlib_skeleton import *

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS


def build_and_send_message(conn:socket, code:str, data:str) -> None:
	"""
	Builds a new message using chatlib, wanted code and message.
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	# Implement Code
	full_msg = build_message(code, data)
	print(f"build_and_send_message: {full_msg}")
	conn.send(full_msg.encode())



def recv_message_and_parse(conn:socket) -> tuple[str, str]:
	"""
	Recieves a new message from given socket,
	then parses the message using chatlib.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If error occured, will return None, None
	"""
	# Implement Code
	full_msg = conn.recv(1024).decode()
	cmd, data = parse_message(full_msg)
	return cmd, data


def build_send_recv_parse(conn:socket, code:str, data:str) -> tuple[str, str]:
	"""Build & Send Message, then Recieve Message & Parse
	by calling: build_and_send_message
	and then: recv_message_and_parse
	:param socket conn: open connection
	:param str code: message code
	:param str data: message data
	:return tuple[str, str]: returns the response message code & data
	"""
	build_and_send_message(conn,code,data)
	msg_code, data = recv_message_and_parse(conn)
	return msg_code, data


def connect() -> socket:
	# Implement Code
	address = (SERVER_IP, SERVER_PORT)
	my_socket = socket(AF_INET, SOCK_STREAM)
	my_socket.connect(address)
	return my_socket


def error_and_exit(error_msg) -> None:
    # Implement code
	print(f"error_and_exit: {error_msg}")
	exit()


def login(conn:socket) -> None:
	while True:
		username = input("Please enter username: ")
		password = input("Please enter password: ")
		# Implement code

		cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["login_msg"],f"{username}#{password}")
		if cmd == PROTOCOL_SERVER["login_ok_msg"]:
			print("User logged in successfully!")
			return
		elif cmd == PROTOCOL_SERVER["login_failed_msg"]:
			print("Login failed!!\n")
		else:
			error_and_exit(cmd)

def get_score(conn:socket) -> None:
	cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["my_score_msg"],"")
	if cmd == PROTOCOL_SERVER["your_score_msg"]:
		print(f"Your score: {data}")
	else:
		print(f"Invalid response: {cmd}")


def get_highscore(conn:socket) -> None:
	cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["highscore_msg"],"")
	if cmd == PROTOCOL_SERVER["all_score_msg"]:
		print(f"High Scores:\n{data}")
	else:
		print(f"Invalid response: {cmd}")


def print_the_question_from_msg_data(msg_data:str) -> int:
	data = msg_data.split("#")
	question_id = data[0]
	question = data[1]
	print(f"({question_id}) {question}?")
	for ans in range(0,4):
		print(f"{ans+1} - {data[ans+2]}")

	return question_id


def play_question(conn:socket) -> None:
	cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_question_msg"],"")
	if cmd == PROTOCOL_SERVER["no_questions_msg"]:
		print(f"No more questions left, game over!!")
	elif cmd == PROTOCOL_SERVER["your_question_msg"]: 
		question_id = print_the_question_from_msg_data(data)
		ans = input("And the answer is?")
		cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["send_answer_msg"],f"{question_id}#{ans}")
		if cmd == PROTOCOL_SERVER["correct_answer_msg"]:
			print("Correct!!")
		elif cmd == PROTOCOL_SERVER["wrong_answer_msg"]:
			print(f"Wrong answer, the correct answer is:{data}")
		else:
			print(f"Invalid response: {cmd}")

	else:
		print(f"Invalid response: {cmd}")


def get_logged_users(conn:socket) -> None:
	cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["logged_in_msg"],"")
	if cmd == PROTOCOL_SERVER["logged_answer_msg"]:
		print("Currently logged in users:")
		logged_in_users = data.split(",")
		for u in range(0,len(logged_in_users)):
			print(f"\t{u+1} - {logged_in_users[u]}")
	else:
		print(f"Invalid response: {cmd}")



def logout(conn:socket):
    # Implement code
	build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"],"")
    


def main():
	conn = connect()
	login(conn)
	while True:
		ans = input("What do you want to do?\n1 - Get my score\n2 - Get high score\n3 - Play question\n4 - Get logged in users\n5 - Quit\n")
		if	ans == "1":
			get_score(conn)
		elif ans == "2":
			get_highscore(conn)
		elif ans == "3":
			play_question(conn)
		elif ans == "4":
			get_logged_users(conn)
		elif ans == "5":
			logout(conn)
			return

if __name__ == '__main__':
    main()
