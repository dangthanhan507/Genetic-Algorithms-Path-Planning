import pygad
import numpy as np
from vector import Vector
from Map import Map

from pygame_visuals import Grid
import pygame
import time

class GA_Solver:
    def __init__(self, MAP, generations: int, parents_mating: int, \
                 solutions_per_pop: int, num_nodes: int, 
                 thresh: (int,int), mutation_percent: int):
        self.generations = generations
        self.parents_mating = parents_mating
        self.sol_per_pop = solutions_per_pop
        
        self.num_genes = num_nodes * 2
        (self.init_range_low, self.init_range_high) = thresh
        self.mutation_percent_genes = mutation_percent
        
        self.ga_instance = None
        self.solution = None
        self.solution_fitness = None
        
        
        
        self.map = MAP
        shape = self.map.get_grid().shape
        self.GRID = Grid(shape[0],shape[1],40,3,start=self.map.get_start(),end=self.map.get_end(), obstacles=[], solution=[])
        
        
    def fitness_func(self, solution, solution_idx):
        penalty = 0
        solution = list(map(int, solution))
        
        grid = self.map.get_grid()
        
        start = self.map.get_start()
        pts = [tuple(solution[i:i+2]) for i in range(0,self.num_genes,2)]
        end = self.map.get_end()
        
        sol_tup = [(solution[i],solution[i+1]) for i in range(0,len(solution),2)]
        
        
        cross_penalty = [9999999999999999 for i in pts if grid[i[::-1]] > 0]
        #print(f'incorrect node selection: {len(cross_penalty)}')
        penalty += sum(cross_penalty)
        
        obstacles_idx = np.where(grid==1)
        obstacles_idx = list(zip(obstacles_idx[1], obstacles_idx[0]))
        
        obs_tup = obstacles_idx
        
        self.GRID.set_obstacles(obs_tup)
        self.GRID.set_solution(sol_tup)
        self.GRID.draw()
        time.sleep(0.5)
        
        dis = 0
        for i in range(len(pts)+1):
            ls_penalty = []
            if i == 0:
                vec = Vector(pts[i][0] - start[0], pts[i][1] - start[1])
                #ls_penalty = [99999999 for j in obstacles_idx if self.map.obstacle_obstructed(start,pts[i], j)]
                for j in obstacles_idx:
                    if self.map.obstacle_obstructed(start,pts[i],j):
                        ls_penalty.append(99999999)
                        #print(f'  Obstructed at point {j}.')
                
                #print(f'penalty of {start} to {pts[i]}: {len(ls_penalty)}')
                penalty += sum(ls_penalty)
            elif i == len(pts):
                vec = Vector(end[0] - pts[i-1][0], end[1] - pts[i-1][1])
                #ls_penalty = [99999999 for j in obstacles_idx if self.map.obstacle_obstructed(pts[i-1],end, j)]
                for j in obstacles_idx:
                    if self.map.obstacle_obstructed(pts[i-1],end,j):
                        ls_penalty.append(99999999)
                        #print(f'  Obstructed at point {j}.')
                #print(f'penalty of {pts[i-1]} to {end}: {len(ls_penalty)}')
                penalty += sum(ls_penalty)
            else:
                vec = Vector(pts[i][0] - pts[i-1][0], pts[i][1] - pts[i-1][1])
                #ls_penalty = [99999999 for j in obstacles_idx if self.map.obstacle_obstructed(pts[i-1],pts[i], j)]
                for j in obstacles_idx:
                    if self.map.obstacle_obstructed(pts[i-1],pts[i],j):
                        ls_penalty.append(99999999)
                        #print(f'  Obstructed at point {j}.')
                
                #print(f'penalty of {pts[i-1]} to {pts[i]}: {len(ls_penalty)}')
                penalty += sum(ls_penalty)
            vec_dis = vec.distance()
            dis += vec_dis
        #print()
        return 1.0 / (dis+penalty)
        
        
    def train_ga(self):
        def fitness_func(solution, solution_idx):
            return self.fitness_func(solution, solution_idx)
        
        
        gene_range = [{'low': self.init_range_low, 'high': self.init_range_high}] * self.num_genes
        
        self.ga_instance = pygad.GA(num_generations = self.generations,
                                   num_parents_mating = self.parents_mating,
                                   fitness_func=fitness_func,
                                    sol_per_pop=self.sol_per_pop,
                                    num_genes=self.num_genes,
                                   init_range_low=self.init_range_low,
                                    gene_space = gene_range,
                                   init_range_high=self.init_range_high,
                                   mutation_percent_genes=self.mutation_percent_genes)
        self.ga_instance.run()
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        
        self.solution = solution
        self.solution_fitness = solution_fitness
    def convert_solution(self):
        solution = list(map(int,self.solution))
        return [tuple(solution[i:i+2]) for i in range(0,self.num_genes,2)]
    
    def produce_sol_grid(self):
        sol = self.convert_solution()
        self.GRID.set_solution(sol)
        self.GRID.draw()
    
    
pygame.init()

obstacles = [(7,0), (8, 0), (9, 0), (4, 3), (0, 4), (1, 4), \
             (3, 4), (4, 4), (0, 5), (1, 5), (3, 5), (4, 5), \
             (7, 7), (8, 7), (7, 8), (8, 8)]

shape = (10,10)
MAP = Map(start=(0,0), end=(9,9), obstacles=obstacles, shape=shape)

ga = GA_Solver(MAP, generations=50, parents_mating=4, solutions_per_pop=100, num_nodes=8, thresh=(0,10), mutation_percent=10)
ga.train_ga()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            running = False