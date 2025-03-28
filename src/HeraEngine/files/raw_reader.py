from HeraEngine.types.Vec2 import Vec2
from HeraEngine.logger import Logger

class BmpReader():
    def __init__(self):
        self.logger = Logger()

    def read_file(self,path):
        
        try: 

            data = []

            with open(path,"r") as file:
                data = file.read().split(";")

            size = Vec2(data[0],data[1])
            data.pop(0)
            data.pop(0)

            for i in range(len(data)):
                data[i] = int(data[i])

            return size, data
        
        except:
            self.logger.WARNING(f"MISSING TEXTURE {path}")
            return (Vec2(2,2),[16465657,0,16465657,0])
