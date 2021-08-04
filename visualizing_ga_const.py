from ga_solver_const import GA_Solver
from Map import Map

import pygame


BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
BLUE = (0,0,200)
GREEN = (0,200,0)
YELLOW = (200,200,0)
PINK = (255,0,255)

pygame.init()

class Square:
    def __init__(self,x,y, size):
        self.x = x
        self.y = y
        self.size = size
    def center(self):
        return tuple(map(int, (self.x + self.size/2, self.y + self.size/2)))
    def draw(self, surface, color):
        pygame.draw.rect(surface, color, pygame.Rect(self.x,self.y,self.size, self.size))
        
    

class Grid:
    def __init__(self, row_blocks, col_blocks, block_size: int, spacing: int, start, end, obstacles, solution):
        #windows = (width, height)
        self.windows = (row_blocks*block_size+(row_blocks-1)*spacing,col_blocks*block_size+(col_blocks-1)*spacing)
        self.surface = pygame.display.set_mode( self.windows )
        self.surface.fill(WHITE)
        self.grid = []
        
        self.start = start
        self.end = end
        
        self.obstacles = obstacles
        self.solution = solution
        for row in range(row_blocks):
            self.grid.append([])
            for col in range(col_blocks):
                x = col*block_size + col*spacing
                y = row*block_size + row*spacing
                sq = Square(x,y,block_size)
                self.grid[row].append(sq)
                
    def draw(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (col,row) == self.start:
                    color = BLUE
                elif (col, row) == self.end:
                    color = GREEN
                elif (col, row) in self.obstacles:
                    color = RED
                elif (col, row) in self.solution:
                    color = YELLOW
                else:
                    color = BLACK
                self.grid[row][col].draw(self.surface, color)
                pygame.display.update()
        
        for i in range(len(solution)+1):
            if i==0:
                start_ix,start_iy = self.start
                start_coord = self.grid[start_iy][start_ix].center()
                
                pt_ix, pt_iy = solution[i]
                pt_coord = self.grid[pt_iy][pt_ix].center()
                
                pygame.draw.line(self.surface, PINK, start_coord, pt_coord, 2)
            elif i == len(solution):
                pt_ix, pt_iy = solution[i-1]
                pt_coord = self.grid[pt_iy][pt_ix].center()
                
                end_ix, end_iy = self.end
                end_coord = self.grid[end_iy][end_ix].center()
                
                pygame.draw.line(self.surface, PINK, pt_coord, end_coord, 2)
            else:
                pt1_ix, pt1_iy = solution[i-1]
                pt1_coord = self.grid[pt1_iy][pt1_ix].center()
                
                pt2_ix, pt2_iy = solution[i]
                pt2_coord = self.grid[pt2_iy][pt2_ix].center()
                
                pygame.draw.line(self.surface, PINK, pt1_coord, pt2_coord, 2)
                
            
            pygame.display.update()
                
                
'''
setting up the MAP environment
'''

obstacles = [(7,0), (8, 0), (9, 0), (4, 3), (0, 4), (1, 4), \
             (3, 4), (4, 4), (0, 5), (1, 5), (3, 5), (4, 5), \
             (7, 7), (8, 7), (7, 8), (8, 8)]

shape = (10,10)
MAP = Map(start=(0,0), end=(9,9), obstacles=obstacles, shape=shape)

'''
GA solves the environment
'''
ga = GA_Solver(MAP, generations=50, parents_mating=20, solutions_per_pop=200, num_nodes=4, thresh=(0,10), mutation_percent=20)
ga.train_ga()

solution = ga.convert_solution()


'''
draw the solution grid
'''
grid = Grid(10,10,50,3,start=(0,0),end=(9,9), obstacles=obstacles, solution=solution)
running = True

grid.draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            running = False
    

