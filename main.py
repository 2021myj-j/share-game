from typing import List, Tuple, Optional

from game.game import App
import confing
from youtube_api import YoutubeLiveChat


class App(App):
    def __init__(self):

        self.frame_counter = 0
        """
        command_list_per_s: List[Tuple[bool, bool]]
        command_list_per_s: List[Tuple[a_pressed, b_pressed]]
        """
        self.command_list: Optional[List[Tuple[bool, bool]]] = None
        self.command_list = [(False, True) for i in range(3)]
        self.youtube_live_chat = YoutubeLiveChat(confing.YOTUBER_URL, confing.YOTUBER_API_KEY)

        super().__init__()

    def update(self):

        self.frame_counter = self.frame_counter % 30
        self.frame_counter += 1
        self.input_command(15)

        super().update()

    def input_command(self, step=1):

        if self.frame_counter % step == step - 1 and not self.command_list:
            self.player.a_pressed, self.player.d_pressed = self.command_list.pop(0)

    def get_command(self):
        return [(True, False) for i in range(6)] + [(False, True) for i in range(6)]


if __name__ == "__main__":
    # youtube_live_chat = YoutubeLiveChat(confing.YOTUBER_URL, confing.YOTUBER_API_KEY)
    App()
