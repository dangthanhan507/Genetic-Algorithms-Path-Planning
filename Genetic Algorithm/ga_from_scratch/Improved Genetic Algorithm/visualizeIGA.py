from IGA import IGA
from Map import Map

import map_lib
from pygame_visuals import Grid
import pygame
pygame.init()

obstacles, shape, MAP = map_lib.map4()

ga = IGA(generations=20, parents_mating=2, init_pop_size=4, MAP=MAP)
ga.train()
solution = ga.solution()
if ga.check_feasibility_path(ga.solution()):
    print('FEASIBLE')
else:
    print('INFEASIBLE')


grid = Grid(shape[0], shape[1], 40, 2, start=MAP.get_start(), \
        end=MAP.get_end(), obstacles=obstacles, solution=solution)
running = True

grid.draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            running = False