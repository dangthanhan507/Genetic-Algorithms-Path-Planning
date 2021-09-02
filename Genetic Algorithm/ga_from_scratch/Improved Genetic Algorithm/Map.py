import numpy as np
from vector import Vector

'''
    Map stores everything. 

'''

class Map:
    def __init__(self, start, end, obstacles, shape=(10,10)):
        '''
            class members:
                grid -> numpy array of 0's and 1's (0 for free, 1 for obstacle)

                starting waypoint
                ending waypoint

                list of obstacles
                list of free space (derived from list of obstacles)
        '''
        self.grid = np.zeros(shape, dtype=np.uint8)
        self.start = start
        self.end = end

        self.grid[start[::-1]] = 2
        self.grid[end[::-1]] = 4

        for i in obstacles:
            self.grid[i[::-1]] = 1

        self.obstacles = obstacles
        self.free_space = [(j,i) for i,j in zip(*np.where(self.grid!=1))]


    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_grid(self):
        return self.grid
    def get_obstacles(self):
        return self.obstacles
    def get_free(self):
        return self.free_space
    
    def set_start(self, start):
        self.start = start
    def set_end(self, end):
        self.end = end 
    def set_grid(self, grid):
        self.grid = grid
    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
    def set_free(self):
        self.free_space = obstacles

