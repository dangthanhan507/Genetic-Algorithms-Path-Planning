from User import User
import pygame


'''
Color coding:
    -gray -> normal tiles
    -black -> obstacles
    -blue -> start
    -green -> end
    -red -> traversed tiles


'''
GRAY = (128,128,128)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,255,0)
GREEN = (0,0,255)

class Square:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class PygameView:
    def __init__(self, user: 'User', display=(800,600), offset=100, padding=5):
        self.display = display
        self.offset = offset
        self.padding = padding
        self.map_dim = (display[0]-100, display[1]-100)

        self.user = user
        self.dimensions = self.user.get_dimensions()
        self.tiles = np.empty(self.dimensions)

        self.corners = {'upper-left': (offset, offset), 'upper-right': (display[0]-offset, offset), 'lower-left': (offset,display[1]-offset), 'lower-right': (display[0]-offset,display[1]-offset)}
        
        self.tile_width = (self.corners['upper-right'][0] - self.corners['upper-left'][0] - self.padding * (self.dimensions[1]-1) ) / self.dimensions[1]
        self.tile_height = (self.corners['lower-right'][1] - self.corners['upper-right'][1] - self.padding * (self.dimensions[0]-1) ) / self.dimensions[0]

        self.surface = pygame.display.set_mode(display)


    def tiles_init(self):
        (x,y) = self.corners['upper-left']
        for i in range(self.tiles.shape[0]):
            x = self.corners['upper-left'][0]
            for j in range(self.tiles.shape[1]):
                self.tiles[i,j] = Square(x,y, self.tile_width, self.tile_height, GRAY)
                x += self.padding
            
            y += self.padding
    
    def draw(self):
        for i in range(self.tiles.shape[0]):
            for j in rnage(self.tiles.shape[1]):
                self.tiles[i,j].draw(self.surface)
        pygame.display.flip()
        