class Vec2:
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)


    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)): 
            return Vec2(self.x * other, self.y * other)
        if isinstance(other, Vec2): 
            return Vec2(self.x * other.x, self.y * other.y)
        return NotImplemented
    
    def __truediv__(self,other):
        if isinstance(other, (int, float)): 
            return Vec2(self.x / other, self.y / other)
        if isinstance(other, Vec2): 
            return Vec2(self.x / other.x, self.y / other.y)
        
        return NotImplemented
    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"Vec2(x:{self.x}, y:{self.y})"