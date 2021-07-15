import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def assigning_edges(Grid: 'Networkx Edgeless Graph', grid_map: 'numpy array',dimensions: (int,int)):
    for row in range(dimensions[0]):
        for col in range(dimensions[1]):
            directions = {'up': True,'down': True,'left': True,'right': True, 'up-left': True, 'up-right': True, 'down-left': True, 'down-right': True}
            #direction removal checks
            if row == 0:
                directions['up'] = False
                directions['up-left'] = False
                directions['up-right'] = False
            if row == dimensions[0]-1:
                directions['down'] = False
                directions['down-left'] = False
                directions['down-right'] = False
            if col == 0:
                directions['left'] = False
                directions['up-left'] = False
                directions['down-left'] = False
            if col == dimensions[1]-1:
                directions['right'] = False
                directions['up-right'] = False
                directions['down-right'] = False

            for direction, tf in directions.items():
                if tf:
                    if directions=='up':
                        Grid.add_edge(grid_map[row,col], grid_map[row-1,col])
                    elif direction=='right':
                        Grid.add_edge(grid_map[row,col], grid_map[row,col+1])
                    elif direction=='down':
                        Grid.add_edge(grid_map[row,col], grid_map[row+1,col])
                    elif direction=='left':
                        Grid.add_edge(grid_map[row,col], grid_map[row,col-1])
                    elif direction=='up-left':
                         Grid.add_edge(grid_map[row,col], grid_map[row-1,col-1])
                    elif direction=='up-right':
                         Grid.add_edge(grid_map[row,col], grid_map[row-1,col+1])
                    elif direction=='down-left':
                         Grid.add_edge(grid_map[row,col], grid_map[row+1,col-1])
                    elif direction=='down-right':
                         Grid.add_edge(grid_map[row,col], grid_map[row+1,col+1])
    return Grid
def generate_grid(row: int, height: int) -> 'Networkx Graph':
    dimensions = (row,height)
    list_grid_map = np.arange(row*height)
    grid_map = list_grid_map.reshape(row,height)
    Grid = nx.Graph()
    Grid.add_nodes_from(list_grid_map)
    
    Grid = assigning_edges(Grid, grid_map, dimensions)
    return Grid
