from Map import Map

class User:
    def __init__(self, Map: 'map', start=0, waypoints=[int]):
        self.map = Map
        self.path = [self.map.get_start()]
        self.path_cost = 0
        self.current_node = self.map.get_start()
        
        self.start = start
        self.waypoints = waypoints
    def get_dimensions(self):
        return self.grid.get_dimensions()
    def get_grid(self):
        return self.grid
    def get_path(self):
        return self.path
    def get_cost(self):
        return self.cost
    def get_current_node(self):
        return self.current_node
    def get_start(self):
        return self.start
    def get_waypoints(self):
        return self.waypoints
    
    def get_current_options(self):
        return self.map.get_node_options(self.current_node)
    def get_traversed(self):
        return [node for node in self.waypoints if node in self.path]
    
    def travel_node(self, node):
        self.path.append(node)
        self.path_cost += 1
        
    def reverse_travel(self):
        del self.path[-1]
        self.path_cost -= 1
    
    
    def reached_end(self):
        for node in self.waypoints:
            if node not in self.path:
                return False
        return True
    def is_stuck(self):
        return len(self.get_current_options())==0