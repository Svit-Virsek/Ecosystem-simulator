import random, pygame
from world import EMPTY, PLANT, ANIMAL

class Animal:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.energy = 100
        self.world.grid[y, x] = ANIMAL
        self.size = 1

    def update(self):
        # --- Step 1: Grow before moving ---
        if self.size == 1 and self.energy >= 1000:
            # Clear old 1x1 footprint
            self.clear_from_grid()
            # Grow
            self.size = 2
            # Clamp top-left anchor so 2x2 fits
            self.x = min(self.x, self.world.width - self.size)
            self.y = min(self.y, self.world.height - self.size)
            # Place new 2x2 footprint
            self.place_on_grid()

        # --- Step 2: Move ---
        self.clear_from_grid()  # clear whatever footprint (size 1 or 2)
        dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.x += dx
        self.y += dy
        # Clamp again after movement
        self.x = max(0, min(self.x, self.world.width - self.size))
        self.y = max(0, min(self.y, self.world.height - self.size))
        self.place_on_grid()

        # Step 3: Energy drain
        self.energy -= 1


    def occupied_cells(self):
        cells = []
        for dy in range(self.size):
            for dx in range(self.size):
                cells.append((self.x + dx, self.y + dy))
        return cells

    def clear_from_grid(self):
        for x, y in self.occupied_cells():
            if 0 <= x < self.world.width and 0 <= y < self.world.height:
                self.world.grid[y, x] = EMPTY

    def place_on_grid(self):
        for x, y in self.occupied_cells():
            if 0 <= x < self.world.width and 0 <= y < self.world.height:
                self.world.grid[y, x] = ANIMAL

    def eat_plant(self):
        self.energy+=100

    def eat_animal(self):
        self.energy+=50


class Plant:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.world.grid[y, x] = PLANT
