import random
import numpy as np
from vector import Vector
from Map import Map
import mapGeometry
import random
class IGA:
    def __init__(self, generations: int, parents_mating: int, init_pop_size: int, MAP: Map):
        '''
            generations = # of generations training will go through
            parents_mating = # of parents that will be selected through selection operator for offsprings 
            pop_size = initial population size

            input:
            output:
        '''
        self.map = MAP # copy of the map to look at
        self.generations = generations
        self.parents_mating = parents_mating

        self.population = []
        self.init_pop_size = init_pop_size

    def get_init_pop_size(self):
        return self.init_pop_size
    def get_population(self):
        return self.population
    def get_pop_size(self):
        return self.pop_size
    def get_parents_mating(self):
        return self.parents_mating
    def get_generations(self):
        return self.generations
    def get_map(self):
        return self.map

    def init_population(self):
        '''
            creates an initial population given a number of individuals wished to be created
            initial population must be feasible
        '''
        start = self.map.get_start()
        end = self.map.get_end()

        grid = self.map.get_grid()
        free_space = self.map.get_free()
        obstacles = self.map.get_obstacles()
        
        self.population = []
        for i in range(self.init_pop_size): 
            path = [start] 
            #creates a visible space to make sure path is feasible
            vi = mapGeometry.visible_space(path[-1], free_space, obstacles) 
            while end not in vi: # don't stop adding nodes until end is reachable
                random_choice = random.randint(0,len(vi)-1)
                path.append(vi[random_choice])
                vi = mapGeometry.visible_space(path[-1], free_space, obstacles)
            path.append(end) 
            self.population.append(path[1:len(path)-1]) #add feasible path to population
        
        self.population = np.array(self.population)

    def path_length(self, chromosome):
        '''


        '''
        start = self.map.get_start()
        end = self.map.get_end()
        length = 0
        for idx_node in range(len(chromosome)+1):
            if idx_node == 0:
                node_x,node_y = chromosome[idx_node]
                prev_x,prev_y = start
            elif idx_node == len(chromosome):
                node_x,node_y = end
                prev_x,prev_y = chromosome[idx_node]
            else:
                node_x,node_y = chromosome[idx_node]
                prev_x,prev_y = chromosome[idx_node-1]

            length += ((node_x-prev_x)**2 + (node_y-prev_y)**2)**0.5 #distance formula
        return length

    def check_feasibility_path(self, path):
        grid = self.map.get_grid()
        obstacles = np.array(list(zip(*np.where(grid==1))))[:,::-1]
        for i in range(len(path)+1):
            #choosing a set of two points to compare if is obstructed
            if i == 0:
                prev_node = self.map.get_start()
                node = path[i]
            elif i == len(path):
                prev_node = path[i-1]
                node = self.map.get_end()
            else:
                prev_node = path[i-1]
                node = path[i]
            
            #any obstacles crossed -> path is infeasible
            if any([mapGeometry.obstacle_obstructed(prev_node,node,obstacle) for obstacle in obstacles]):
                return False
        return True

    def random_node_selection(self, chromosome):
        '''

        '''
        start = self.map.get_start()
        end = self.map.get_end()

        random_select_idx = random.randint(0,len(chromosome)-1)
        random_select = chromosome[random_select_idx]

        if random_select_idx == 0: #if it is at very start, include starting waypoint as neighbor
            neighbor_back = start
            neighbor_front = chromosome[random_select_idx + 1]
        elif random_select_idx == len(path)-1: #if it is at very end, include ending waypoint as neighbor
            neighbor_back = chromosome[random_select_idx - 1]
            neighbor_front = end
        else: #else treat neighbors at indices left and right
            neighbor_back = chromosome[random_select_idx - 1]
            neighbor_front = chromosome[random_select_idx + 1]
        
        return (neighbor_back, random_select, random_select_idx, neighbor_front) #returns node + node idx + neighbors
    def fitness_function(self, chromosome):
        '''

        '''
        return 1 / self.path_length(chromosome)
    def fitness(self): #calculating basic fitness function
        '''

        '''
        return np.array([self.fitness_function(chromosome) \
                        for chromosome in self.population])

    def selection(self): #roulette selection operator
        #uses parents_mating parameter
        '''
            roulette selection operator using parents_mating as 
            parameter to choose # offsprings mated
        '''
        fitness_pop = self.fitness()
        p_weights = fitness_pop / np.sum(fitness_pop)
        return np.random.choice(self.population, self.parents_mating, p=p_weights, replace=False)

    def crossover(self): #single-point crossover operator
        '''

        '''
        parents = self.population
        assert parents.shape >= 2
        assert parents.shape%2 == 0
        assert parents[0].shape[0] != 0

        offsprings = []
        for path in range(0,parents.shape[0], 2): #iterate every other path
            parent1_idx, parent2_dx = i, i+1
            crossover_point = max(parents[parent1_idx].shape[0], \
                                    parents[parent2_idx].shape[0]) // 2
            offspring_path1 = parents[parent1_idx][0:crossover_point] + parents[parent2_idx][crossover_point:]
            offspring_path2 = parents[parent2_idx][0:crossover_point] + parents[parent1_idx][crossover_point:]

        return np.array(offspring, dtype=object) #return np array of offsprings

    def mutation_add(self): #custom 3-point add mutation
        '''

        '''
        start = self.map.get_start()
        end = self.map.get_end()


        for chromosome in self.population: #iterating through each path
            back_node, rand_node, rand_idx, front_node = random_node_selection(chromosome, start,end)

            #list of grids traversed from line from behind node to node
            grids_back2curr = mapGeometry.bresenham(back_node, rand_node) 
            # lsit of grids traversed from line from node to front of node.
            grids_curr2front = mapGeometry.bresenham(rand_node, front_node) 

            len_grids_back2curr = len(grids_back2curr)
            len_grids_curr2front = len(grids_curr2front)

            if len_grids_back2curr == 0:
                add_back2curr_node = back_node
            else:
                back2curr_idx = random.randint(0, len_grids_back2curr-1)
                add_back2curr_node = grids_back2curr[back2curr_idx]
            
            if len_grids_curr2front == 0:
                add_curr2front_node = front_node
            else:
                curr2front_idx = random.randint(0, len_grids_curr2front-1)
                add_curr2front_node = grids_curr2front[curr2front_idx]
        #doesn't need return since the lists (references) are modified within np.array 
        #so the population is modified

    def mutation_remove(self): #custom 1-point removal mutation
        '''

        '''
        size = self.population.shape[0]
        modif_path = []

        start = self.map.get_start()
        end = self.map.get_end()
        for i in range(size):
            path = self.population[i]
            init, random_select, random_select_idx, final = self.random_node_selection(path,start,end)
            if not any([mapGeometry.obstacle_obstructed(init,final,obstacle) for obstacle in self.get_obstacles()]):
                path.pop(random_select_idx)

    def train(self): #training chromosomes of the IGA
        '''
        '''
        #for iteration in range(self.generations):
        pass



    #get/set operators