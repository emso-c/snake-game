from .snake import Snake
from .board import Board
from .game_controller import GameController
from .direction import Direction
from .globals import MIN_DELAY

class Game:
    def __init__(self, board:Board, snake:Snake, delay:float, verbose:bool=True, disable_gui:bool=False) -> None:
        if delay <= MIN_DELAY:
            raise ValueError("invalid delay")
        self.controller = GameController(board, snake, delay, verbose)
        self.disable_gui = disable_gui

    def render(self):
        self.controller.render_snake()
        self.controller.put_borders()
        self.controller.delayed_render()

    def move(self, direction:Direction=None):
        if direction:
            self.controller.change_direction(direction)
        self.controller.move_snake()
        if not self.disable_gui:
            self.render()
