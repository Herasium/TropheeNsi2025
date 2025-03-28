
class Color():
    def __init__(self,r=0,g=0,b=0):
        self.r = r
        self.g = g
        self.b = b

        self.value = self.get_int()

    def get_int(self):
        return (self.r << 16) | (self.g << 8) | self.b
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.value = self.get_int()