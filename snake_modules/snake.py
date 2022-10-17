from .coordinate import Coordinate
from .direction import Direction

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
