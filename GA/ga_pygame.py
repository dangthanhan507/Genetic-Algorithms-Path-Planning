from ga_solver_const import GA_Solver
from Map import Map

import map_lib
from pygame_visuals import Grid
import pygame

pygame.init()

obstacles, shape, MAP = map_lib.map2()


ga = GA_Solver(MAP, generations=40, parents_mating=4, solutions_per_pop=50, num_nodes=8, thresh=(0,16), mutation_percent=10)
ga.train_ga()
solution = ga.convert_solution()


grid = Grid(shape[0], shape[1], 40, 2, start=MAP.get_start(), end=MAP.get_end(), obstacles=obstacles, solution=solution)
running = True

grid.draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            running = False