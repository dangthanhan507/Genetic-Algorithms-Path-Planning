import pygad
import numpy as np
from vector import Vector
from Map import Map
'''
This file contains the classes and software necessary to work create a genetic algorithm solver for a grid.
This is based on a constant amount of nodes that the genetic algorithm has to work with.
'''

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
        
    def fitness_func(self, solution, solution_idx):
        penalty = 0
        solution = list(map(int, solution))
        
        grid = self.map.get_grid()
        
        start = self.map.get_start()
        pts = [tuple(solution[i:i+2]) for i in range(0,self.num_genes,2)]
        end = self.map.get_end()
        
        
        cross_penalty = [9999999999999999 for i in pts if grid[i[::-1]] > 0]
        #print(f'incorrect node selection: {len(cross_penalty)}')
        penalty += sum(cross_penalty)
        
        obstacles_idx = np.where(grid==1)
        obstacles_idx = list(zip(obstacles_idx[1], obstacles_idx[0]))
        
        
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
        grid = np.copy(self.map.get_grid())
        for i in sol:
            grid[i[::-1]] = 5
        return grid