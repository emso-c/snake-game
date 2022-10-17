import os
from .graphic import Graphic
from .coordinate import Coordinate

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
