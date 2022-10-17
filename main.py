from dataclasses import dataclass
import random
import os
from time import sleep, time
import keyboard
from datetime import datetime
import json

MIN_DELAY = 0.02
PLAYER_NAME = "test"
STORAGE_PATH = "./storage/scores.json"

class IllegalDirectionError(ValueError):
    """Raises when direction is illegal"""

@dataclass
class Coordinate:
    x: int
    y: int

    def __repr__(self):
        return f'Coordinate({self.x}, {self.y})'

class Direction:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Graphic:
    EMPTY = '.'
    TARGET = 'O'
    BORDER_Y = "|"
    BORDER_X = "_"
    SNAKE_BODY = '#'
    SNAKE_HEAD_UP = "^"
    SNAKE_HEAD_DOWN = "v"
    SNAKE_HEAD_RIGHT = ">"
    SNAKE_HEAD_LEFT = "<"


class Snake:
    def __init__(self, length: 3, initial_pos: Coordinate):
        self.length = length
        self.pos = [Coordinate(initial_pos.x, initial_pos.y + i) for i in range(length)]
        self.direction = Direction.RIGHT

    @property
    def tail(self):
        return self.pos[0]

    @property
    def head(self):
        return self.pos[-1]

        
class Board:
    def __init__(self, area:tuple):
        self.area = area
        self.cells = self.empty_board()

    def empty_board(self):
        return [[Graphic.EMPTY for _ in range(self.area[1])] for _ in range(self.area[0])]

    def get_cell_value(self, coordinate:Coordinate):
        return self.cells[coordinate.x][coordinate.y]

    def render(self):
        os.system("cls")
        for row in self.cells:
            print(''.join(row))
        print()

class Verbose:
    def __init__(self, verbose:bool):
        self.verbose = verbose

    def vprint(self, *args):
        if self.verbose:
            print(*args)

class GameController(Verbose):
    def __init__(self, board:Board, snake:Snake, delay:float, verbose:bool=True):
        super().__init__(verbose)
        self.board = board
        self.snake = snake
        self.delay = delay
        self.score = 0
        self.eat_timer = int(time())+10
        self.current_time = 0
        self.player = PLAYER_NAME
        self.save_location = STORAGE_PATH

        self.target = self.get_random_target()
        self.render_snake()
        self.put_borders()
        self.put_target()

    def save_stats(self):
        try:
            with open(self.save_location, "r") as file:
                data:list = json.load(file)
        except:
            with open(self.save_location, 'w') as file:
                file.write("[]")
            data = []
        with open(self.save_location, 'w+') as file:
            data.append({
                "player": self.player,
                "score": self.score,
                "time": datetime.now()
            })
            json.dump(data, file, indent=4, default=str)
        
    def load_stats(self):
        try:
            with open(self.save_location, "r") as file:
                return json.load(file) # file has to include at least "[]"
        except:
            return []

    def change_direction(self, direction:Direction):
        if  (self.snake.direction is Direction.LEFT and direction is Direction.RIGHT) or \
            (self.snake.direction is Direction.RIGHT and direction is Direction.LEFT) or \
            (self.snake.direction is Direction.DOWN and direction is Direction.UP) or \
            (self.snake.direction is Direction.UP and direction is Direction.DOWN):
            #raise IllegalDirectionError
            return
            
        self.snake.direction = direction

    def move_snake(self):
        next_pos = None
        if self.snake.direction == Direction.LEFT:
            next_pos = Coordinate(self.snake.head.x, self.snake.head.y-1)
        elif self.snake.direction == Direction.RIGHT:
            next_pos = Coordinate(self.snake.head.x, self.snake.head.y+1)
        elif self.snake.direction == Direction.UP:
            next_pos = Coordinate(self.snake.head.x-1, self.snake.head.y)
        elif self.snake.direction == Direction.DOWN:
            next_pos = Coordinate(self.snake.head.x+1, self.snake.head.y)
        else:
            raise ValueError("Invalid move (You shouldn't be seeing this)")
    
        next_pos_val = self.board.get_cell_value(next_pos) 
        if next_pos_val is Graphic.TARGET:
            self.snake.pos.append(next_pos)
            self.target = self.get_random_target()
            self.score += (10/self.delay)
            self.eat_timer = int(time())+10
            self.delay -= (self.delay/10)
            if self.delay <= MIN_DELAY:
                self.delay = MIN_DELAY
            return
        if next_pos_val not in [Graphic.EMPTY, Graphic.TARGET]:
            self.vprint("Game over")
            print(self.score)
            high_score = max([stat["score"] for stat in self.load_stats()] or [0])
            if self.score >= high_score:
                self.vprint("NEW HIGH SCORE!") 
            self.save_stats()
            exit()
        self.snake.pos.append(next_pos)
        self.snake.pos.pop(0)

    def _is_all_full(self):
        for x in range(self.board.area[0]):
            for y in range(self.board.area[1]):
                if self.board.cells[x][y] == Graphic.EMPTY:
                    return False
        return True

    def get_random_target(self):
        if self._is_all_full():
            raise Exception('All places are full')
        while True:
            x = random.randint(0, self.board.area[0] - 1)
            y = random.randint(0, self.board.area[1] - 1)
            if self.board.cells[x][y] is Graphic.EMPTY:
                return [x, y]

    def put_target(self):
        self.board.cells[5][10] = Graphic.TARGET
    
    def put_borders(self):
        for row in self.board.cells:
            row[0] = Graphic.BORDER_Y
            row[-1] = Graphic.BORDER_Y

        self.board.cells[0] = [Graphic.BORDER_X]*self.board.area[1]
        self.board.cells[-1] = [Graphic.BORDER_X]*self.board.area[1]
        
        self.board.cells[self.target[0]][self.target[1]] = Graphic.TARGET

    def render_snake(self):
        self.board.cells = self.board.empty_board() # workaround for deleting tail, bad practice
        for pos in self.snake.pos:
            self.board.cells[pos.x][pos.y] = Graphic.SNAKE_BODY
        self.board.cells[self.target[0]][self.target[1]] = Graphic.TARGET

        if self.snake.direction == Direction.DOWN:
            head_direction = "v"
        if self.snake.direction == Direction.UP:
            head_direction = "^"
        if self.snake.direction == Direction.RIGHT:
            head_direction = ">"
        if self.snake.direction == Direction.LEFT:
            head_direction = "<"
        self.board.cells[pos.x][pos.y] = head_direction

    def delayed_render(self):
        self.board.render()
        curr_time = int(time())
        if curr_time > self.eat_timer:
            self.target = self.get_random_target()
            self.eat_timer = int(time())+10
            self.score -= (10/self.delay)/3
        sleep(self.delay)

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

def handle_up_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.UP)

def handle_right_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.RIGHT)

def handle_left_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.LEFT)

def handle_down_key(e:keyboard.KeyboardEvent):
    game.controller.change_direction(Direction.DOWN)

if __name__ == "__main__":
    game = Game(
        board = Board(area=(20, 40)),
        snake = Snake(length=4, initial_pos=Coordinate(3, 3)),
        delay = .2,
        verbose=True,
        disable_gui=True
    )

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
