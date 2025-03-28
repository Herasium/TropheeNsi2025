from HeraEngine.childs.Entity import Entity
from HeraEngine.types.Font import Font
from HeraEngine.types.Vec2 import Vec2

class Text(Entity):

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self.is_text = True
        self._text = value
        self._len = len(self._text)

        if getattr(self,"_font",None) != None:
            self.size = Vec2(self._font.size.x*self._len,self._font.size.y)

    
    @property
    def font(self):
        return self._font
    
    @font.setter
    def font(self,value):
        if not isinstance(value,Font):
            raise TypeError("Target should be a Font")
        
        self._font = value
        self.size = Vec2(self._font.size.x*self._len,self._font.size.y)

