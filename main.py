import pygame
import numpy as np
import random
from creatures import Animal, Plant
from world import World, EMPTY, PLANT, ANIMAL
pygame.init()

# ---------------- Settings ----------------
CELL_SIZE = 15
WORLD_WIDTH = 120
WORLD_HEIGHT = 50
NUM_PLANTS = 150
NUM_ANIMALS = 200
FPS = 10
FONT = pygame.font.Font(None, 100)

# ---------------- Pygame Setup ----------------
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH * CELL_SIZE, WORLD_HEIGHT * CELL_SIZE))
pygame.display.set_caption("Mini Ecosystem Simulation")
clock = pygame.time.Clock()
systemcollapse = FONT.render("System Collapsed", True, (255, 255, 255))
systemcollapse_rect = systemcollapse.get_rect(center=(WORLD_WIDTH*CELL_SIZE/2, WORLD_HEIGHT*CELL_SIZE/2))
try_again = FONT.render("Try again", True, (255, 255, 255))
try_again_rect = try_again.get_rect(center=(WORLD_WIDTH*CELL_SIZE/2, WORLD_HEIGHT*CELL_SIZE/1.5))

# ---------------- World Setup ----------------
def restart(WORLD_WIDTH, WORLD_HEIGHT, NUM_PLANTS, NUM_ANIMALS):
    global animals, plants, world
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    # Spawn plants
    plants = []
    for _ in range(NUM_PLANTS):
        x, y = world.random_empty_cell()
        plants.append(Plant(world, x, y))

    # Spawn animals
    animals = []
    for _ in range(NUM_ANIMALS):
        x, y = world.random_empty_cell()
        animals.append(Animal(world, x, y))

restart(WORLD_WIDTH, WORLD_HEIGHT, NUM_PLANTS, NUM_ANIMALS)

# ---------------- Main Loop ----------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if try_again_rect.collidepoint(event.pos):
                restart(WORLD_WIDTH, WORLD_HEIGHT, NUM_PLANTS, NUM_ANIMALS)

    # Update animals
    for animal in animals:
        animal.update()

    #add creatures
    if(random.randrange(1, 100)>0):
        if(random.randrange(1, 2)==2):
            x, y = world.random_empty_cell()
            animals.append(Animal(world, x, y))
        else:
            x, y = world.random_empty_cell()
            plants.append(Plant(world, x, y))

    # Draw
    screen.fill((30, 30, 30))  # background
    for y in range(world.height):
        for x in range(world.width):
            cell = world.grid[y, x]
            if cell == PLANT:
                pygame.draw.rect(screen, (0, 200, 0),
                                 (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == ANIMAL:
                pygame.draw.rect(screen, (220, 220, 220),
                                 (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for i in reversed(range(len(animals))):
        animal = animals[i]

        # --- Eat plants in all occupied cells ---
        for x, y in animal.occupied_cells():
            if 0 <= x < world.width and 0 <= y < world.height:
                if world.grid[y, x] == PLANT:
                    animal.eat_plant()
                    # remove plant from list safely
                    for n in reversed(range(len(plants))):
                        if plants[n].x == x and plants[n].y == y:
                            del plants[n]
                            world.grid[y, x] = EMPTY  # clear the grid
                            i+=1

        # --- Eat other animals in all occupied cells ---
        for x, y in animal.occupied_cells():
            if 0 <= x < world.width and 0 <= y < world.height:
                if world.grid[y, x] == ANIMAL:
                    for n in reversed(range(len(animals))):
                        other = animals[n]
                        if other != animal and (other.x, other.y) in other.occupied_cells():
                            if x in range(other.x, other.x + other.size) and y in range(other.y, other.y + other.size):
                                animal.eat_animal()
                                other.clear_from_grid()
                                del animals[n]
                                world.grid[y, x] = EMPTY
                                i+=1
        if(animals[i].energy==0 or animals[i].energy>2000):
            animals[i].clear_from_grid()
            del animals[i]

    if(len(animals)==0 or len(plants)==0):
        screen.blit(systemcollapse, systemcollapse_rect)
        screen.blit(try_again, try_again_rect)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
