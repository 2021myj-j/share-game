# import datetime
from typing import List, Tuple, Optional

from game.game import App
# from utils import update_func  # , confing
"""
def add_instance_var(self):
    self.frame_counter = 0


def input_command(self):

    global command_list

    if self.counttime.microseconds < 975000:
        return

    if not command_list:
        command_list = get_command()

    self.player.a_pressed, self.player.d_pressed = command_list.pop(0)


def get_command():
    return [(True, False) for i in range(6)] + [(False, True) for i in range(6)]
"""


class App(App):
    def __init__(self):

        self.frame_counter = 0
        """
        command_list_per_s: List[Tuple[bool, bool]]
        command_list_per_s: List[Tuple[a_pressed, b_pressed]]
        """
        self.command_list: Optional[List[Tuple[bool, bool]]] = None
        self.command_list = [(False, True) for i in range(3)]

        super().__init__()

    def update(self):

        self.frame_counter = self.frame_counter % 30
        self.frame_counter += 1
        self.input_command(15)

        super().update()

    def input_command(self, step=1):

        if self.frame_counter % step == step - 1:

            if not self.command_list:
                self.command_list = self.get_command()

            self.player.a_pressed, self.player.d_pressed = self.command_list.pop(0)

    def get_command(self):
        return [(True, False) for i in range(6)] + [(False, True) for i in range(6)]


if __name__ == "__main__":
    """
    command_list_per_s: List[Tuple[bool, bool]]
    command_list_per_s: List[Tuple[a_pressed, b_pressed]]
    """
    # command_list: Optional[List[Tuple[bool, bool]]] = None

    # command_list = [(False, True) for i in range(3)]

    # execution_before_update = [input_command]
    # execution_after_update = []

    # execution_before_init = [add_instance_var]
    # execution_after_init = []

    # App.update = update_func(
    #     App.update,
    #     before=execution_before_update,
    #     after=execution_after_update
    # )  # yapf: disable

    # App.__init__ = update_func(
    #     App.__init__,
    #     before=execution_before_init,
    #     after=execution_after_init
    # )  # yapf: disable

    App()
