from HeraEngine.types.Vec2 import Vec2
from HeraEngine.types.Vec3 import Vec3
from HeraEngine.types.Color import Color
from HeraEngine.types.Texture import Texture
from HeraEngine.types.BoxCollision import BoxCollision

class Entity:
    def __init__(self, layer, size, position,core= None, **kwargs):
        if layer not in {1, 2, 3, 4}:
            raise ValueError("Unknown Layer")

        if None in {size, position}:
            raise ValueError("Missing Size or Position")

        is_flat = layer in {1, 3, 4}
        expected_type = Vec2 if is_flat else Vec3

        if not isinstance(size, expected_type) or not isinstance(position, expected_type):
            raise TypeError(f"Size and Position should be of type {expected_type.__name__}")

        self.layer = layer
        self._size = size
        self._position = position
        self.dimentional = not is_flat
        self.flat = is_flat
        self.color = Color(255,255,255)
        self._texture = None
        self._core = core
        self.textured = False
        self.is_text = False
        self.rotation = 0

        self.hitbox = BoxCollision(self._position,self._size)
        
        if "text" in kwargs:
            self.text = kwargs["text"]
            
        if "font" in kwargs:
            self.font = kwargs["font"]

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self,size):
        expected_type = Vec2 if self.flat else Vec3

        if not isinstance(size, expected_type):
            raise TypeError(f"Size should be a {expected_type.__name__}")
        
        self._size = size
        self.hitbox.size = self._size

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,position):
        expected_type = Vec2 if self.flat else Vec3

        if not isinstance(position, expected_type):
            raise TypeError(f"Position should be a {expected_type.__name__}")
        
        self._position = position
        self.hitbox.position = self._position

    @property   
    def texture(self):
        return self._texture
    
    @texture.setter
    def texture(self,path):
        if isinstance(path,str):
            self._texture = Texture(path,self._core)
            self.textured = True
            self._texture.size = self.size
        elif isinstance(path,Texture):
            self._texture = path
            self.textured = True
            self._texture.size = self.size
        else:
            raise TypeError("Path should be a str or a Texture object.")

    def collide(self,target):
        if not isinstance(target,Entity):
            raise TypeError("Target is not an Entity")
        
        return self.hitbox.collide(target.hitbox)