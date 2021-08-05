'''
Just a big library of maps that will be used in the simulations.
'''

def original_map():
    obstacles = [(7,0), (8, 0), (9, 0), (4, 3), (0, 4), (1, 4), \
             (3, 4), (4, 4), (0, 5), (1, 5), (3, 5), (4, 5), \
             (7, 7), (8, 7), (7, 8), (8, 8)]
    shape = (10,10)
    MAP = Map(start=(0,0), end=(9,9), obstacles=obstacles, shape=shape)
    
    
    return (obstacles, shape, MAP)
