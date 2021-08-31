import numpy as np
from vector import Vector
'''
0 -> free space
1 -> obstacle
2 -> start
4 -> end
'''

class Map:
    def __init__(self, start, end, obstacles, shape = (10,10)):
        self.grid = np.zeros(shape, dtype=np.uint8)
        self.start = start
        self.end = end
        
        self.grid[start[::-1]] = 2
        self.grid[end[::-1]] = 4
        
        for i in obstacles:
            self.grid[i[::-1]] = 1
    
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_grid(self):
        return self.grid
    
    def set_start(self, val: (int,int)):
        self.grid[self.start[::-1]] = 0
        self.start = val
        self.grid[start[::-1]] = 2
        
    def set_end(self, val: (int,int)):
        self.grid[self.end[::-1]] = 0
        self.end = val
        self.grid[self.end[::-1]] = 4
    def set_grid(self, val: 'Grid'):
        self.grid = val
    
    def obstacle_threshold(self, start: (int,int), obstacle: (int,int)): # (x,y) returns (low, high)
        obj_vec = Vector(abs(obstacle[0] - start[0]) , abs(obstacle[1] - start[1]))
        
        tl = obj_vec + Vector(-0.5,0.5)
        tr = obj_vec + Vector(0.5,0.5)
        bl = obj_vec + Vector(-0.5,-0.5)
        br = obj_vec + Vector(0.5,-0.5)
        
        
        ls_angle = np.array([i.angle() for i in [tl,tr,bl,br]])

        min_ls_angle = min(ls_angle)
        max_ls_angle = max(ls_angle)
        return (min_ls_angle, max_ls_angle)
    
    def sign(self, x):
        if x>=0:
            return 1
        else:
            return -1

    def obstacle_obstructed(self, start: (int,int), end: (int,int), obstacle: (int,int)):
        traj_vector = Vector(end[0] - start[0], end[1] - start[1])
        obj_vector = Vector(end[0] - obstacle[0], end[1] - obstacle[1])
        
        dot = traj_vector * obj_vector

        if dot <= 0: #if it is at or in front of obstacle, then is gud
            return False

        sig_x = self.sign(obj_vector.x)
        sig_y = self.sign(obj_vector.y)
        traj_vector.x *= sig_x
        traj_vector.y *= sig_y

        obj_vector.x *= sig_x
        obj_vector.y *= sig_y

        angle_traj = traj_vector.angle()
        threshold = self.obstacle_threshold(start, obstacle)

        return threshold[0] <= angle_traj <= threshold[1]
