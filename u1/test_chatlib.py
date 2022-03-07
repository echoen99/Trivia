import chatlib_skeleton as chatlib
import unittest


class Test_ChatLib_BuildMessage(unittest.TestCase):
    def test_build_valid_input_normal_message(self):
        self.assertEqual(chatlib.build_message("LOGIN", "aaaa#bbbb"), "LOGIN           |0009|aaaa#bbbb")

    def test_build_valid_input_normal_message_single_data(self):
        self.assertEqual(chatlib.build_message("LOGIN", "aaaabbbb"), "LOGIN           |0008|aaaabbbb")

    def test_build_zero_length_message(self):
        self.assertEqual(chatlib.build_message("LOGIN", ""), "LOGIN           |0000|")

    def test_build_zero_length_message(self):
        self.assertEqual(chatlib.build_message("LOGIN", ""), "LOGIN           |0000|")

    def test_build_invalid_input_cmd_too_long(self):
        self.assertEqual(chatlib.build_message("0123456789ABCDEFG", ""), None)

    def test_build_invalid_input_message_too_long(self):
        self.assertEqual(chatlib.build_message("A", "A"*(chatlib.MAX_DATA_LENGTH+1)), None)

class Test_ChatLib_ParseMessage(unittest.TestCase):
    def test_parse_valid_input_normal_message(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |   9|aaaa#bbbb"), ("LOGIN", "aaaa#bbbb"))

    def test_parse_valid_input_normal_message_cmd_indent(self):
        self.assertEqual(chatlib.parse_message(" LOGIN          |   9|aaaa#bbbb"), ("LOGIN", "aaaa#bbbb"))

    def test_parse_valid_input_normal_message_cmd_fully_indent(self):
        self.assertEqual(chatlib.parse_message("           LOGIN|   9|aaaa#bbbb"), ("LOGIN", "aaaa#bbbb"))

    def test_parse_valid_input_normal_message_data_size_position(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |9   |aaaa#bbbb"), ("LOGIN", "aaaa#bbbb"))

    def test_parse_valid_input_normal_message_data_size_value_prefixed(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |  09|aaaa#bbbb"), ("LOGIN", "aaaa#bbbb"))

    def test_parse_valid_input_normal_message_data_size_value_fully_prefixed(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |0009|aaaa#bbbb"), ("LOGIN", "aaaa#bbbb"))

    def test_parse_valid_input_normal_shorter_message(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |   9| aaa#bbbb"), ("LOGIN", " aaa#bbbb"))

    def test_parse_valid_input_normal_short_data(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |   4|data"), ("LOGIN", "data"))

    def test_parse_invalid_input_missing_1st_delimiter(self):
        self.assertEqual(chatlib.parse_message("LOGIN           x	  4|data"), (None, None))

    def test_parse_invalid_input_missing_2nd_delimiter(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |	  4xdata"), (None, None))

    def test_parse_invalid_input_negative_data_size(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |	 -4|data"), (None, None))

    def test_parse_invalid_input_invalid_data_size(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |	  z|data"), (None, None))

    def test_parse_invalid_input_incorrect_data_size(self):
        self.assertEqual(chatlib.parse_message("LOGIN           |	  5|data"), (None, None))

if __name__ == '__main__':
    unittest.main()
