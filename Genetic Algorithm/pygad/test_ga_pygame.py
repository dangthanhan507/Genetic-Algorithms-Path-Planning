from ga_solver_const import GA_Solver
from Map import Map


from pygame_visuals import Square, Grid
import pygame

pygame.init()
             
                
'''
setting up the MAP environment
'''

obstacles = [(7,0), (8, 0), (9, 0), (4, 3), (0, 4), (1, 4), \
             (3, 4), (4, 4), (0, 5), (1, 5), (3, 5), (4, 5), \
             (7, 7), (8, 7), (7, 8), (8, 8)]

shape = (10,10)
MAP = Map(start=(0,0), end=(9,9), obstacles=obstacles, shape=shape)

'''
GA solves the environment
'''
ga = GA_Solver(MAP, generations=100, parents_mating=50, solutions_per_pop=100, num_nodes=8, thresh=(0,10), mutation_percent=10)
ga.train_ga()


solution = ga.convert_solution()

'''
draw the solution grid
'''
grid = Grid(10,10,50,3,start=(0,0),end=(9,9), obstacles=obstacles, solution=solution)
running = True

grid.draw()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            running = False
    