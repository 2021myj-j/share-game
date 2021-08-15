from copy import deepcopy
from functools import wraps
from typing import Optional
from youtube_api import YoutubeLiveChat
import confing
import time


def add_operation(before: list = [], after: list = []):
    def add_operation_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            for before_fuc in before:
                before_fuc(*args, **kwargs)

            res = func(*args, **kwargs)

            for after_fuc in after:
                after_fuc(*args, **kwargs)

            return res

        return wrapper

    return add_operation_decorator


def update_func(origin, before: list = [], after: list = []):
    """
    Add some processing before and after the execution of the original function. Returns a new function.

    This function contains the following parameters

    origin:     The original function
    before:     A list of functions. These functions will be executed !!before!! the original function
    after:      A list of functions. These functions will be executed !!after!! the original function
    """

    origin = deepcopy(origin)

    @add_operation(before, after)
    @wraps(origin)
    def new_func(*args, **kwargs):
        origin(*args, **kwargs)

    return new_func


class ChatToCommand():
    def __init__(self, fps=30) -> None:

        self.valid_command_str = ("a", "A", "d", "D", "y", "Y")

        self.valid_command = {
            "a": (True, False, False),
            "A": (True, False, False),
            "d": (False, True, False),
            "D": (False, True, False),
            "y": (False, False, True),
            "Y": (False, False, True)
        }

        self.fps = fps

    def str_to_command(self, string):
        if string not in self.valid_command_str:
            return

        return self.valid_command[string]

    def count_pattern(self, string: str, pattern):
        res_of_count = string.count(pattern)
        return res_of_count

    def count_a(self, string, capital: Optional[bool] = None):

        if capital is not None:
            if capital:
                count = self.count_pattern(string, "A")
            else:
                count = self.count_pattern(string, "a")
        else:
            count = self.count_pattern(string, "A") + self.count_pattern(string, "a")

        return count

    def count_d(self, string, capital: Optional[bool] = None):

        if capital is not None:
            if capital:
                count = self.count_pattern(string, "D")
            else:
                count = self.count_pattern(string, "d")
        else:
            count = self.count_pattern(string, "D") + self.count_pattern(string, "d")

        return count

    def count_y(self, string, capital: Optional[bool] = None):

        if capital is not None:
            if capital:
                count = self.count_pattern(string, "Y")
            else:
                count = self.count_pattern(string, "y")
        else:
            count = self.count_pattern(string, "Y") + self.count_pattern(string, "y")

        return count

    def get_first_valid_command(self, string):
        for i in string:
            if i in self.valid_command_str:
                return i

    def first_valid_command_str_to_command(self, string):
        return self.str_to_command(self.get_first_valid_command(string))

    def compare_commands_vec2(self, string):
        return self.count_a(string) - self.count_d(string)

    def get_bool_commands_vec2(self, string) -> Optional[bool]:
        commands_vec2 = self.compare_commands_vec2(string)
        if not commands_vec2:
            return None
        elif commands_vec2 > 0:
            return True
        else:
            return False

    def data_to_num_of_command(self, data):
        command_srt_list = []
        for i in data["comments"]:
            display_message = i["display_message"]
            command_srt_list.append(
                {
                    "a": self.count_a(display_message),
                    "d": self.count_d(display_message),
                    "y": self.count_y(display_message),
                    "vec2": self.count_a(display_message) - self.count_d(display_message)
                }
            )

        return command_srt_list

    def data_set_to_num_of_command(self, data):
        count_a, count_d, count_y = 0, 0, 0
        for i in data["comments"]:
            display_message = i["display_message"]
            count_a += self.count_a(display_message)
            count_d += self.count_d(display_message)
            count_y += self.count_y(display_message)

        return {
            "a": count_a,
            "d": count_d,
            "y": count_y,
        }

    def get_command_list(self, fps, data):
        pass
        # is_y_pressed = False

        # if self.data_set_to_num_of_command(data)["y"] > 0:
        #     is_y_pressed = True

        # num_of_command_list = self.data_to_num_of_command(data)

        # if is_y_pressed
        # if len(data["comments"]) == fps:
        #     pass


if __name__ == '__main__':
    string = "abcdDDefgaaAAayYya"
    string2 = "54564"
    pattern = "a"
    chat_to_command = ChatToCommand()

    # count_ans = []
    # count_ans.append(chat_to_command.count_pattern(string, pattern))
    # count_ans.append(chat_to_command.count_a(string))
    # count_ans.append(chat_to_command.count_a(string, True))
    # count_ans.append(chat_to_command.count_d(string))
    # count_ans.append(chat_to_command.count_y(string))
    # count_ans.append(chat_to_command.count_y(string2, True))
    # count_ans.append(chat_to_command.first_valid_command_str_to_command(string))
    # count_ans.append(chat_to_command.first_valid_command_str_to_command(string2))

    youtube_live_chat = YoutubeLiveChat(
        confing.YOTUBER_URL, confing.YOTUBER_API_KEY, interval=5
    )
    while True:
        data = youtube_live_chat.get_next_chat_message(
            nextPageToken="GPuO1sP7sfICIITO1M77sfIC"
        )
        print(data["next_page_token"])
        for i in data["comments"]:
            display_message = i["display_message"]
            print(display_message)

        num_of_command = chat_to_command.data_to_num_of_command(data)
        print(num_of_command)
        time.sleep(10)

    # for i in count_ans:
    #     print(i)
