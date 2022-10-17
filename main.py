import keyboard

from snake_modules.game import Game
from snake_modules.coordinate import Coordinate
from snake_modules.snake import Snake
from snake_modules.board import Board
from snake_modules.direction import Direction
from snake_modules.exceptions import IllegalDirectionError


game = Game(
    board = Board(area=(20, 40)),
    snake = Snake(length=4, initial_pos=Coordinate(3, 3)),
    delay = .2,
    verbose=True,
    disable_gui=False
)

def handle_up_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.UP)

def handle_right_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.RIGHT)

def handle_left_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.LEFT)

def handle_down_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.DOWN)

if __name__ == "__main__":
    keyboard.on_press_key('up', handle_up_key)
    keyboard.on_press_key('down', handle_down_key)
    keyboard.on_press_key('left', handle_left_key)
    keyboard.on_press_key('right', handle_right_key)

    while True:
        try:
            game.move()
            if keyboard.is_pressed('q'):
                break
        except IllegalDirectionError:
            break
