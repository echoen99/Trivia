# Protocol Constants
from dataclasses import fields


CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
# Max size of data field according to protocol
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + \
    1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_in_msg": "LOGGED",
    "my_score_msg": "MY_SCORE",
    "highscore_msg": "HIGHSCORE",
    "get_question_msg": "GET_QUESTION",
    "send_answer_msg": "SEND_ANSWER",
}  # .. Add more commands if needed


PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "logged_answer_msg": "LOGGED_ANSWER",
    "your_score_msg": "YOUR_SCORE",
    "all_score_msg": "ALL_SCORE",
    "your_question_msg" : "YOUR_QUESTION",
    "correct_answer_msg": "CORRECT_ANSWER",
    "wrong_answer_msg": "WRONG_ANSWER",
    "no_questions_msg": "NO_QUESTIONS",
    "server_error": "ERROR"

}  # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def left_pan(text: str, to_length: int, symbol: chr) -> str:
    """returns the text left panned with symbol
    :param str text: the text
    :param int to_length: required length
    :param chr symbol: one char symbol for panning
    :raises ValueError: length of text is bigger than requested length
    :return str: returns the text left panned with symbol
    """
    length_of_text = len(text)
    if (length_of_text > to_length):
        raise ValueError(
            f"Text:{text} is bigger then requested length:{to_length}")
    left_panned_text = symbol*(to_length - length_of_text) + text
    return left_panned_text


def right_pan(text: str, to_length: int, symbol: chr) -> str:
    """returns the text right panned with symbol
    :param str text: the text
    :param int to_length: required length
    :param chr symbol: one char symbol for panning
    :raises ValueError: length of text is bigger than requested length
    :return str: returns the text right panned with symbol
    """
    length_of_text = len(text)
    if (length_of_text > to_length):
        raise ValueError(
            f"Text:{text} is bigger then requested length:{to_length}")
    right_panned_text = text + symbol*(to_length - length_of_text)
    return right_panned_text


def trailing_zeros(num: int, to_length: int):
    return left_pan(str(num), to_length, "0")


def leading_spaces(text: str, to_length: int):
    return right_pan(text, to_length, " ")


def build_message(cmd: str, data: str):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    # Implement code ...
    try:
        message = [leading_spaces(cmd, CMD_FIELD_LENGTH), trailing_zeros(
            len(data), LENGTH_FIELD_LENGTH), data]
        full_msg = DELIMITER.join(message)
    except:
        full_msg = None

    return full_msg


def parse_message(data: str):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    # Implement code ...
    try:
        full_message = data.split(DELIMITER)
        cmd = full_message[0].strip()
        data_size = int(full_message[1])
        data = full_message[2]
        if data_size<0:
            raise ValueError(f"Invalud data size:{data_size}")
        if data_size>len(data):
            raise ValueError(f"Data size:{data_size} is less than actuall data length:{len(data)}")

        msg = data[0: data_size]
    except:
        cmd = msg = None
    # The function should return 2 values
    return cmd, msg


def split_data(msg: str, expected_fields):
    """
    Helper method. gets a string and text of expected fields in it. Splits the string 
    using protocol's data field delimiter (|#) and validates that there are correct text of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    # Implement code ...
    count_delimiters_in_msg = msg.count(DATA_DELIMITER)
    if count_delimiters_in_msg != expected_fields:
        return [None]

    list_of_fields = msg.split(DATA_DELIMITER)  # ,expected_fields
    return list_of_fields


def join_data(msg_fields: list):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
    Returns: string that looks like cell1#cell2#cell3
    """
    # Implement code ...
    return DATA_DELIMITER.join(msg_fields)
