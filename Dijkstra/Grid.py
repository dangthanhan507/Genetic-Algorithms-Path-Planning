from grid_generation import *

class Grid:
    def __init__(self, row=3, height=3):
        self.grid = generate_grid(row,height)
        
        self.dimensions = (row,height)
        
        self.grid_map = np.arange(row*height)
        self.grid_map.reshape(row,height)
        
        
        self.obstacles = {}
    def get_grid(self):
        return self.grid
    def get_dimensions(self):
        return self.dimensions
    def get_grid_map(self):
        return self.grid_map
    def get_node_options(self, node):
        return list(self.grid[node])
    
    def add_node(self, edges: [int]):
        new_node = self.dimensions[0] * self.dimensions[1]
        self.grid.add_node(new_node)
        for i in edges:
            self.grid.add_edge(new_node, i)
        
    def add_edge(self, edge):
        self.grid.add_edge(*edge)
        
    def add_obstacle(self, node):
        self.obstacles[node] = list(self.grid[node])
        self.remove_node(node)
        
    def remove_node(self, node):
        self.grid.remove_node(node)
        
    def remove_edge(self, edge):
        self.grid.remove_edge(*edge)

    def remove_obstacle(self, node):
        self.grid.add_node(node)
        for i in self.obstacles[node]:
            self.add_edge( (node, i) )
        self.obstacles.pop(node, None)
            
    def raw_draw(self):
        nx.draw(self.grid, with_labels=True, font_weight='bold')