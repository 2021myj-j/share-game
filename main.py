from typing import List, Tuple, Optional

from game.game import App
import confing
from youtube_api import YoutubeLiveChat
from utils import ChatToCommand


class App(App):
    def __init__(self, debug_mode=False):

        self.frame_counter = 0
        """
        command_list_per_s: List[Tuple[bool     , bool     , bool     ]]
        command_list_per_s: List[Tuple[a_pressed, b_pressed, y_pressed]]
        """
        self.command_list: Optional[List[Tuple[bool, bool, bool]]] = []
        # self.command_list = [(False, True) for i in range(3)]
        self.youtube_live_chat = YoutubeLiveChat(
            confing.YOTUBER_URL, confing.YOTUBER_API_KEY, interval=1
        )
        self.chat_to_command = ChatToCommand()
        super().__init__(debug_mode)

    def update(self):

        self.frame_counter = self.frame_counter % 30
        self.frame_counter += 1
        self.get_command()
        self.input_command(1)

        super().update()

    def input_command(self, step=1):
        if step < 1 or step > 30:

            class OutStepRange(Exception):
                def __str__(self) -> str:
                    return "out of step randge. The range of steps is 1-30."

            raise OutStepRange

        if self.frame_counter % step == step - 1 and self.command_list:
            self.player.a_pressed, self.player.d_pressed, self.player.y_pressed = self.command_list.pop(0)  # yapf: disable

    def get_command(self):
        next_chat_message = self.youtube_live_chat.get_next_chat_message()

        if not next_chat_message or (len(next_chat_message["comments"]) == 0):
            if next_chat_message:
                print("---empty!---")
            return

        is_y_pressed = False
        if self.chat_to_command.data_set_to_num_of_command(next_chat_message)["y"] > 0:
            is_y_pressed = True

        if is_y_pressed:
            self.command_list.append(self.chat_to_command.str_to_command("y"))

        num_of_command_list = self.chat_to_command.data_to_num_of_command(next_chat_message)  # yapf: disable

        for i in num_of_command_list:

            if i["vec2"] > 0:
                for j in range(i["vec2"]):
                    self.command_list.append(self.chat_to_command.str_to_command("a"))
            elif i["vec2"] < 0:
                for j in range(-i["vec2"]):
                    self.command_list.append(self.chat_to_command.str_to_command("d"))

        for i in next_chat_message["comments"]:
            display_message = i["display_message"]
            print(display_message)

        #     first_valid_command = self.chat_to_command.first_valid_command_str_to_command(display_message)   # yapf: disable
        #     if first_valid_command:
        #         self.command_list.append(first_valid_command)


if __name__ == "__main__":
    # youtube_live_chat = YoutubeLiveChat(confing.YOTUBER_URL, confing.YOTUBER_API_KEY)
    print("\n\n\n")
    App(debug_mode=True)
