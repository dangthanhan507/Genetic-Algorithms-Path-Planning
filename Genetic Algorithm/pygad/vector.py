import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if type(other) is int or type(other) is float:
            return Vector(self.x + other, self.y + other)
        elif type(other) is Vector:
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
    
    def angle(self):
        return math.atan2(self.y,self.x) * 180 / math.pi
    
    def distance(self):
        return (self.x**2 + self.y**2)**(0.5)