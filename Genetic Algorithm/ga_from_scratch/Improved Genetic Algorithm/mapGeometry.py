import numpy as np 
from vector import Vector

def obstacle_threshold(start: (int,int), obstacle: (int,int)):
    '''
        takes in a starting waypoint and obstacle in a mxn grid.
        creates angle threshold that if within start, means obstacle may be obstructive.

        input:
            start (x,y): (int,int)
            obstacle (x,y): (int,int)
        output:
            threshold: (min_theta, max_theta): (float,float)
    '''
    obj_vec = Vector(abs(obstacle[0] - start[0]) , abs(obstacle[1] - start[1]))


    tl = obj_vec + Vector(-0.5,0.5)
    tr = obj_vec + Vector(0.5,0.5)
    bl = obj_vec + Vector(-0.5,-0.5)
    br = obj_vec + Vector(0.5,-0.5)

    ls_angle = np.array([i.angle() for i in [tl,tr,bl,br]])

    return (min(ls_angle), max(ls_angle))

def sign(x): return 1 if x>=0 else -1


def obstacle_obstructed(start: (int,int), end: (int,int), obstacle: (int,int)):
    '''
        takes in a start and end point and creates a waypoint from start to end.
        checks to see if the obstacle is obstructing the path of the line.

        
        input:
            start: (x,y) : (int,int)
            end: (x,y) : (int,int)
            obstacle: (x,y) : (int,int)
        output:
            True -> obstructs
            False -> does not obstruct
            
            boolean
    '''
    #traj_vector: line vector from start to end
    #obj_vector: line vector from start to obstacle
    traj_vector = Vector(end[0] - start[0], end[1] - start[1])
    obj_vector = Vector(obstacle[0] - start[0], obstacle[1] - start[1])

    dot = traj_vector * obj_vector

    if dot <= 0: #if it is at or in front of obstacle, then is gud
        return False

    sig_x = sign(obj_vector.x)
    sig_y = sign(obj_vector.y)
    traj_vector.x *= sig_x
    traj_vector.y *= sig_y

    obj_vector.x *= sig_x
    obj_vector.y *= sig_y

    angle_traj = traj_vector.angle()
    threshold = obstacle_threshold(start, obstacle)

    return threshold[0] <= angle_traj <= threshold[1]

def visible_space(start: (int,int), free_space: [(int,int)], obstacles: [(int,int)]):
    '''
        given a current position and map of surroundings, generates possible waypoints to travel to.
        input:
            start: (int,int)
            free_space: [(int,int)]
            obstacles [(int,int)]

            Note: free_space and obstacles should be mutually exclusive
        output:
            list of waypoints that can be travelled
            [(int,int)]
    '''
    return [space for space in free_space \
        if not np.any([obstacle_obstructed(start, space, obstacle) \
            for obstacle in obstacles])]

def visible_space_set(start: (int,int), free_space: [(int,int)], obstacles: [(int,int)]):
    '''
        same as visible_space but returns a set instead of a list
    '''
    return {space for space in free_space \
        if not np.any([obstacle_obstructed(start, space, obstacle) \
            for obstacle in obstacles])}

def bresenham(point0, point1):

    '''
        integer calculation of grids traversed with line using line interpolation
        and other math stuffs.

        input: (x0,y0) and (x1,y1)
        output: list of grids traversed
    '''
    x0,y0 = point0
    x1,y1 = point1

    if x1-x0 == 0:
        dy = y1-y0
        sig = 1 if dy > 0 else -1
        path_list = [(x0,y0+sig*i) for i in range(sig*dy+1)]
    elif y1-y0 == 0:
        dx = x1-x0
        sig = 1 if dx > 0 else -1
        path_list = [(x0+sig*i,y0) for i in range(sig*dx+1)]
    else:
        dx = abs(x1-x0)
        sx = 1 if x0<x1 else -1
        dy = -abs(y1-y0)
        sy = 1 if y0 < y1 else -1
        err = dx+dy
        path_list = []
        x = x0
        y = y0
        while (x != x1 or y != y1):
            path_list.append( (x,y) )
            e2 = 2*err
            if (e2>=dy):
                err += dy
                x += sx
            if (e2 <= dx):
                err += dx
                y += sy

        path_list.append( (x,y) )
    
    path_list.remove( (x0,y0) )
    path_list.remove( (x1,y1) )
    return path_list