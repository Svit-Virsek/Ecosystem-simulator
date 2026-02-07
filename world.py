import numpy as np
import random

EMPTY = 0
PLANT = 1
ANIMAL = 2

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.int8)

    def random_empty_cell(self):
        while True:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            if self.grid[y, x] == EMPTY:
                return x, y
