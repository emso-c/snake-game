from dataclasses import dataclass

@dataclass
class Coordinate:
    x: int
    y: int

    def __repr__(self):
        return f'Coordinate({self.x}, {self.y})'