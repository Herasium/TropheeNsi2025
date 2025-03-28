import threading
import traceback
import time
import os
import ctypes

from HeraEngine.logger import Logger
from HeraEngine.childs.Entity import Entity
from HeraEngine.render.pipeline import PipeLine
from HeraEngine.cursor import Cursor
from HeraEngine.keyboard import Keyboard
from HeraEngine.benchmark import benchmark
from HeraEngine.files.TextureLoader import TextureLoader
from HeraEngine.popup import Popup

from HeraEngine.types.Vec2 import Vec2

class Core():
    def __init__(self,start,update,asset_path):

        self.ascii_art = """
Powered by HeraEngine"""

        self.os = os.name
        self.is_windows = self.os == "nt"
        self.running = False
        self.EntityList = {1:[],2:[],3:[],4:[]}
        self.entity_count = 0
        self._fullscreen = False
        self._size = Vec2(1920,1080)
        self._asset_path = asset_path
        
        self._categorize_cpu_score = lambda score: 1 if score >= 9 else 2 if score >= 7 else 3 if score >= 3 else 4

        self.ver = "1.0.4"

        self.log = Logger()
        self.Pipeline = PipeLine(self)
        self.cursor = Cursor()
        self.keyboard = Keyboard()
        self.clear = False
        
        self.log.INFO(self.ascii_art)
        
        self.cpu_score = benchmark()
        self.log.INFO(f"Ran cpu benchmark. Score: {self.cpu_score}")
        self.tick_update = 1
        self.log.DEBUG(f"Current tick update: {self.tick_update}")
        
        self.texture_loader = TextureLoader(self._asset_path,self)
        self.texture_loader.read_all()
        self.texture_loader.load_all()

        self.basic_screen_size = Vec2(1920,1080)
        self.target_ratio = 16/9

        self.tick_count = 0
        self.fps = 60
        self.fps_total = 0
        self.average_fps = 0
        self.fps_tick = 0
        

        if self.is_windows:
            self.log.DEBUG(f"Detected platform: Windows, importing window")
            from HeraEngine.window import Window
            self.window = Window(self,self.size,self.cursor,self.keyboard)
            self.log.DEBUG(f"Loaded Window Size: {self.window.Size}")

        else:
            self.log.DEBUG(f"Detected platform: Unix (Max/Linux), importing pygame_adapter")
            from HeraEngine.pygame_adapter import Window
            self.window = Window(self,self.size,self.cursor,self.keyboard)
            self.log.DEBUG(f"Loaded Window (PyGame Adapter) Size: {self.window.Size}")

        self.start = start
        self.update = update

    def calculate_max_dimensions(self,width, height, ratio):
        max_height = width / ratio
        if max_height > height:
            max_width = height * ratio
            return Vec2(max_width, height)
        else:
            return Vec2(width, max_height)

    @property
    def fullscreen(self):
        return self._fullscreen
    
    @fullscreen.setter
    def fullscreen(self,value):
        self._fullscreen = value
        self.window.fullscreen = value
        fullsize = self.window.GetFullscreenSize()
        self.size = Vec2(fullsize[0],fullsize[1])
        self.ratio = fullsize[1]/fullsize[0]
        self.log.INFO(f"Launched Game in fullscreen. Basic Size: {self.basic_screen_size}, Target Size: {self.size}")
        self.log.INFO(f"Basic ratio: {self.target_ratio}, Target ration: {self.ratio}")
        if self.ratio != self.target_ratio:
            self.size = self.calculate_max_dimensions(self.size.x,self.size.y,self.target_ratio)
            self.log.INFO(f"New max size with ratio: {self.size}")
            self.Pipeline.target_size=self.size

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self,value):
        if not isinstance(value, Vec2):
            raise TypeError(f"Size should be a Vec2, not {value.__class__.__name__}")
        self._size = value
        self.Pipeline.update(size=self._size) 
        self.Pipeline.clear_buffer()

    def add_entity(self,target):
        if isinstance(target,Entity):
            self.EntityList[target.layer].append(target)
        else:
            raise TypeError("Target is not an Entity.")
        
        self.update_entity_count()

    def update_entity_count(self):
        self.entity_count = 0
        for i in self.EntityList:
            self.entity_count += len(self.EntityList[i])

    def remove_entity(self,target):
        if target in self.EntityList[1]:
            self.EntityList[1].remove(target)
        if target in self.EntityList[2]:
            self.EntityList[2].remove(target)
        if target in self.EntityList[3]:
            self.EntityList[3].remove(target)
        if target in self.EntityList[4]:
            self.EntityList[4].remove(target)

        self.update_entity_count()

    def run(self):
        try:
            self.running = True
            self.log.DEBUG("Launching Start function")
            self.start(self)
            update_thread = threading.Thread(target=self.run_updates)
            update_thread.daemon = True
            update_thread.start()
            self.log.DEBUG("Launched Update thread.")
            self.window.MainWin()
            self.log.INFO("Code Ended. Goodbye ;)")

        except SystemExit:
                raise
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)[-1]
            message = f"{e} - L.{tb.lineno} - {tb.filename}"
            traceback.print_exc()
            self.log.ERROR(f"Failed to start: {message}")
            self.error(message,2)
            raise BaseException(f"Failed to start: {message}")

    def run_updates(self, max_fps=100):

        while self.running:
            try:
                start_time = time.time()

                # Actual update and rendering logic
                self.cursor.update()
                self.keyboard.update()
                self.update(self)  # Run the update function
                self.Pipeline.update(EntityList=self.EntityList)  # Update pipeline
                self.Pipeline.render()  # Render the frame
                self.window.buffer = self.Pipeline.BackgroundBuffer  # Update window data
                self.window.update()  # Draw window

                if self.clear:
                    self.Pipeline.clear_buffer()  # Clear buffer if necessary

                self.keyboard.last_pressed = []
                
                # Calculate execution time
                end_time = time.time()
                execution_time = end_time - start_time
                execution_time = max(execution_time, 1e-8)  # Prevent division by zero

                self.fps = 1 / execution_time
                self.tick_count += self.tick_update
                self.fps_total += self.fps
                self.fps_tick += 1

                if self.fps_tick > 20:
                    self.average_fps = self.fps_total / self.fps_tick
                    self.fps_total = 0
                    self.fps_tick = 0

            except SystemExit:
                raise
            except Exception as e:
                tb = traceback.extract_tb(e.__traceback__)[-1]
                message = f"{e} - L.{tb.lineno} - {tb.filename}"
                traceback.print_exc()
                self.log.ERROR(f"Failed to update: {message}")
                self.error(message, 1)
                raise BaseException(f"Failed to update: {message}")

    def error(self,error,code):
        self.window.kill = True
        Popup(f"Une erreur s'est produite : {error}\nNous sommes désolés de la gêne occasionnée.\nMerci de bien vouloir redémarrer le jeu.",f"HeraEngine Crash Code: {code}",1)
    def quit(self):
        self.window.kill = True
        Popup("Merci d'avoir joué à notre jeu. Nous vous souhaitons une bonne journée/soirée.","HeraEngine Exit Code:0",4)
        quit(0)
        
    def reset_fps_average(self):
        self.tick_count = 0
        self.fps_total = 0