import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
BLUE = (0,0,200)
GREEN = (0,200,0)
YELLOW = (200,200,0)
PINK = (255,0,255)

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
    
    def get_obstacles(self):
        return self.obstacles
    def get_solution(self):
        return self.solution
    
    def set_obstacles(self, val):
        self.obstacles = val
    def set_solution(self, val):
        self.solution = val
    
    def draw(self):
        self.surface.fill(WHITE)
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
        if self.solution != []:
            for i in range(len(self.solution)+1):
                if i==0:
                    start_ix,start_iy = self.start
                    start_coord = self.grid[start_iy][start_ix].center()

                    pt_ix, pt_iy = self.solution[i]
                    pt_coord = self.grid[pt_iy][pt_ix].center()

                    pygame.draw.line(self.surface, PINK, start_coord, pt_coord, 2)
                elif i == len(self.solution):
                    pt_ix, pt_iy = self.solution[i-1]
                    pt_coord = self.grid[pt_iy][pt_ix].center()

                    end_ix, end_iy = self.end
                    end_coord = self.grid[end_iy][end_ix].center()

                    pygame.draw.line(self.surface, PINK, pt_coord, end_coord, 2)
                else:
                    pt1_ix, pt1_iy = self.solution[i-1]
                    pt1_coord = self.grid[pt1_iy][pt1_ix].center()

                    pt2_ix, pt2_iy = self.solution[i]
                    pt2_coord = self.grid[pt2_iy][pt2_ix].center()

                    pygame.draw.line(self.surface, PINK, pt1_coord, pt2_coord, 2)

            
            pygame.display.update()
