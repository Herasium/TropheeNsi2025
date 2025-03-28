from HeraEngine.types.Vec2 import Vec2

class BoxCollision():
    def __init__(self,position,size):

        if not isinstance(position,Vec2):
            raise TypeError("Box position should be a Vec2.")

        if not isinstance(size,Vec2):
            raise TypeError("Box size should be a Vec2.")

        self._position = position
        self._size = size

        self._rect = [self._position.x,self._position.y,self._position.x + self._size.x,self._position.y + self._size.y]

    @property
    def rect(self):
        return self._rect
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self,size):
        if not isinstance(size,Vec2):
            raise TypeError("Size should be a Vec2")
        
        self._size = size
        self._rect = [self._position.x,self._position.y,self._position.x + self._size.x,self._position.y + self._size.y] 

    @property
    def position(self):
        return self._position
    
    @size.setter
    def position(self,position):
        if not isinstance(position,Vec2):
            raise TypeError("Position should be a Vec2")
        
        self._position = position
        self._rect = [self._position.x,self._position.y,self._position.x + self._size.x,self._position.y + self._size.y]
    
    def collide(self,other):
        if not isinstance(other,BoxCollision):
            raise TypeError("Target to collide is not a BoxCollision.")
        
        x_overlap = max(self.rect[0], other.rect[0]) < min(self.rect[2], other.rect[2])
        y_overlap = max(self.rect[1], other.rect[1]) < min(self.rect[3], other.rect[3])

        return x_overlap and y_overlap