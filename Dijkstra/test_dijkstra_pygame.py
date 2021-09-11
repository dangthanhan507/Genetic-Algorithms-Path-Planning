import pygame_visuals
import pygame

from Map import Map
import Grid

import networkx as nx

'''
    generate the map
'''
obstacles = [(7,0), (8, 0), (9, 0), (4, 3), (0, 4), (1, 4), \
             (3, 4), (4, 4), (0, 5), (1, 5), (3, 5), (4, 5), \
             (7, 7), (8, 7), (7, 8), (8, 8)]

shape = (10,10)
MAP = Map(start=(0,0), end=(9,9), obstacles=obstacles, shape=shape)

'''
    solve using dijkstra's algorithms
'''
GRID = Grid.Grid(10,10)

idx_obstacles = [x+10*y for x,y in obstacles]

for i in idx_obstacles:
    GRID.add_obstacle(i)

start = MAP.get_start()
start = start[0] + start[1]*10

end = MAP.get_end()
end = end[0] + end[1]*10

idx_solution = nx.dijkstra_path(GRID.grid, start, end)

solution = [(i%10 ,i//10) for i in idx_solution]

'''
    pygame create grid
'''
pygame.init()
grid = pygame_visuals.Grid(10,10,50,3,start=MAP.get_start(),end=MAP.get_end(), obstacles=obstacles, solution=solution)
running = True

grid.draw()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            running = False
    
