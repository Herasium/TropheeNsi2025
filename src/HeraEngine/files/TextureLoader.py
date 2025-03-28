from HeraEngine.files.raw_reader import BmpReader
from HeraEngine.logger import Logger
from HeraEngine.types.Vec2 import Vec2

import os   

class TextureLoader:
    def __init__(self,asset_folder,core):
        self._reader = BmpReader()
        self._core = core
        self._asset_path = asset_folder
        self._path_list = []
        
        self.logger = Logger()
        
        self.data = {}
        
    def read_all(self):
        file_list = []
        for root, _, files in os.walk(self._asset_path):
            for file in files:
                if file.endswith(".raw") or file.endswith(".raw.corrupted"):
                    file_list.append(os.path.join(root, file))
        self._path_list = file_list
        
    def load_all(self):
        for i in self._path_list:
            data = self._reader.read_file(i)
            self.data[i]=data
            self.logger.DEBUG(f"Loaded file {i}")
            
    def get_texture(self,path):
        if self._core.is_windows:
            path = path.replace("/","\\")
        else:
            path = path.replace("\\","/")
        if path in self.data:
            return self.data[path]
        else:
            self.logger.WARNING(f"MISSING TEXTURE {path}")
            return (Vec2(2,2),[16465657,0,16465657,0])