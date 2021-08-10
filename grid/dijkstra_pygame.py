import pygame_visuals
import pygame

import map_lib

from Map import Map
import Grid

import networkx as nx

pygame.init()

obstacles, shape, MAP = map_lib.map4()

GRID = Grid.Grid(shape[0],shape[1])

idx_obstacles = [x+shape[0]*y for x,y in obstacles]

for i in idx_obstacles:
    GRID.add_obstacle(i)

    
start = MAP.get_start()
start = start[0] + start[1]*shape[0]

end = MAP.get_end()
end = end[0] + end[1]*shape[0]

    
idx_solution = nx.dijkstra_path(GRID.grid, start, end)

solution = [(i%shape[1] ,i//shape[0]) for i in idx_solution]


grid = pygame_visuals.Grid(shape[0],shape[1],45,3,start=MAP.get_start(),end=MAP.get_end(), obstacles=obstacles, solution=solution)
running = True

grid.draw()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            running = False
