from HeraEngine import *
import math
import random
import asyncio

from MiniGames.tree import Tree
from MiniGames.road import Road
from MiniGames.maze import Maze
from MiniGames.pacman import PacMan
from MiniGames.pacman_corrupted import PacManCorrupted
from MiniGames.puzzle import Puzzle
from Transitions.dream_2 import Dream2
from Transitions.dream_3 import Dream3
from Transitions.dream_4 import Dream4
from Transitions.dream_4_corrupted import Dream45
from Cutscenes.scene_1 import Scene1
from Cutscenes.scene_2 import Scene2
from Cutscenes.scene_3 import Scene3
from Cutscenes.scene_4 import Scene4

class Game:
    def __init__(self, app: Core,corrupted = False):
        

        self.app = app
        self.current_next = getattr(self.app,"next",0)
        self.sound = Sound("Assets/Audio/musique.mp3")

        self.corrupted = corrupted
        self._in_transition = False
        self._setup_app_properties()
        self._create_attributes()
        self._create_collections() 
        self._setup_entities()
        self._setup_event_handlers()


        if getattr(self.app,"to_dream",0) != 0:
            self.technical_collection.quit()
            self.bg_collection.quit()
            match int(getattr(self.app,"to_dream",0)):
                case 2:
                    Dream2(self.app)
                case 3:
                    Scene1(self.app).setup()
                case 4:
                    Scene2(self.app).setup()
                case 45:             
                    Scene3(self.app).setup()

            self.app.to_dream = 0

        


    def _setup_app_properties(self):
        self.app.window.Title = "Once uppon a Dream."
        self.app.clear = False
        self.app.fullscreen = True

    def _create_attributes(self):
        self.game_ver = "0.0.2"
        self.app.monogram = Font("Monogram")
        self.app.monogram.size = Vec2(x=13, y=28)
        self.app.monogram.offset = Vec2(-2, 0)
        
        self.app.monogram_big = Font("MonogramBig")
        self.app.monogram_big.size = Vec2(x=48, y=48)
        self.app.monogram_big.offset = Vec2(-28, 0)
        
        self.app.monogram_corrupted = Font("Monogram",corrupted=True)
        self.app.monogram_corrupted.size = Vec2(x=13, y=28)
        self.app.monogram_corrupted.offset = Vec2(-2, 0)
        
        self.app.monogram_big_corrupted = Font("MonogramBig",corrupted=True)
        self.app.monogram_big_corrupted.size = Vec2(x=48, y=48)
        self.app.monogram_big_corrupted.offset = Vec2(-28, 0)

    def _create_collections(self):
        self.bg_collection = Collection(self.app)
        self.technical_collection = Collection(self.app)

    def _setup_entities(self):
        self.technical_collection.Entity(
            "background", layer=layers.background,
            size=Vec2(1920, 1080), position=Vec2(0, 0),
            color=Color(0, 0, 0)
        )
        self._add_background_entities()
        self._add_menu_entities()
        self._add_technical_entities()

    def _add_background_entities(self):
        if self.corrupted:
            textures = [
                ("background", "1.raw.corrupted"), ("stars", "2.raw.corrupted"),("behind_clouds_copy", "3.raw.corrupted"),   ("behind_clouds", "3.raw.corrupted"),("front_clouds", "4.raw.corrupted"),("front_clouds_copy", "4.raw.corrupted")
            ]
        else:
            textures = [
                ("background", "1.raw"), ("stars", "2.raw"),("behind_clouds_copy", "3.raw"),   ("behind_clouds", "3.raw"),("front_clouds", "4.raw"),("front_clouds_copy", "4.raw")
            ]
            
        positions = [Vec2(0, 0)] * 4 + [Vec2(1920, 0)] * 2
        
        for i, (name, tex) in enumerate(textures):
            self.bg_collection.Entity(
                name, layer=layers.background,
                size=Vec2(1920, 1080), position=positions[i],
                texture=f"Assets/Textures/Clouds/4/{tex}")

    def _add_menu_entities(self):
        if self.corrupted:
            menu_items = [
                ("main_menu_title", 630, 81, 40, 285, "title.raw.corrupted"),
                ("main_menu_play", 200, 63, 40, 600, "play.raw.corrupted"),
            ]
        
        else:
            menu_items = [
                ("main_menu_title", 630, 81, 40, 285, "title.raw"),
                ("main_menu_play", 200, 63, 40, 600, "play.raw"),
                ("main_menu_quit", 266, 80, 40, 685, "quit.raw")
            ]
        
        for name, w, h, x, y, tex in menu_items:
            self.bg_collection.Entity(
                name, layer=layers.background,
                size=Vec2(w, h), position=Vec2(x, y),
                texture=f"Assets/Textures/Menus/Main/{tex}")

    def _add_technical_entities(self):
        self.technical_collection.Text(
            "fps_counter", layer=layers.background,
            size=Vec2(100, 28), position=Vec2(0, 0),
            text="Hello World!", font=self.app.monogram)
        
        self.technical_collection.Text(
            "version_display", layer=layers.background,
            size=Vec2(100, 28), position=Vec2(0, 20),
            text=f"Once Upon a Dream {self.game_ver} ; HeraEngine {self.app.ver}",
            font=self.app.monogram)
        

        self.technical_collection.Entity(
            "cursor_tracker", layer=layers.background,
            size=Vec2(0, 0), position=Vec2(0, 0))
        self.technical_collection.cursor_tracker.hitbox.size = Vec2(1, 1)

    def _setup_event_handlers(self):
        self.app.cursor.on_right_click.append(self.on_click)
        self.app.cursor.on_left_click.append(self.on_click)

    def on_click(self, cursor):
        if not self._in_transition:
            if getattr(self.bg_collection,"main_menu_quit",None) != None:
                if self.technical_collection.cursor_tracker.collide(self.bg_collection.main_menu_quit):
                    self.app.quit()
            if self.technical_collection.cursor_tracker.collide(self.bg_collection.main_menu_play):
                self._in_transition = True
                self.start_count = self.app.tick_count
                for i in self.bg_collection.entity_list:
                        entity = self.bg_collection.entity_list[i]
                        entity.start_x = entity.position.y

    def update(self,*args):
        if not self._in_transition:
            self._update_cloud_positions()
            self._update_cursor_tracking()
            self._update_menu_animation()
            self._update_fps_counter()
        else:
            if (self.app.tick_count - self.start_count) <= 400:
                self._update_cloud_positions()
                count = 0
                for i in self.bg_collection.entity_list:
                    entity = self.bg_collection.entity_list[i]
                    entity.position = Vec2(entity.position.x,reverse_elastic_interpolation(entity.start_x,entity.start_x+1080,(self.app.tick_count - (self.start_count+10*count))/200))
                    count += 1
            else:
                self.technical_collection.quit()
                self.bg_collection.quit()
                if self.corrupted:
                    Scene4(self.app).setup()
                elif self.current_next == 0:
                    self.tree = Tree(self.app)
                    self.tree.setup()
                elif self.current_next == 1:
                    self.road = Dream2(self.app)
           
                elif self.current_next == 2:
                    self.maze = Dream3(self.app)
                    
                elif self.current_next == 4:
                    self.pacman = Dream4(self.app)
                
                elif self.current_next == 45:
                    self.corrupted = Dream45(self.app)
              
                else:   
                    self.tree = Tree(self.app)
                    self.tree.setup()



    def _update_cloud_positions(self):
        count = self.app.tick_count % 1920
        count_dup = (self.app.tick_count / 2) % 1920
        
        self.bg_collection.behind_clouds.position = Vec2(0 - count_dup, self.bg_collection.behind_clouds.position.y)
        self.bg_collection.front_clouds.position = Vec2(0 - count, self.bg_collection.front_clouds.position.y)
        self.bg_collection.behind_clouds_copy.position = Vec2(1920 - count_dup, self.bg_collection.behind_clouds_copy.position.y)
        self.bg_collection.front_clouds_copy.position = Vec2(1920 - count, self.bg_collection.front_clouds_copy.position.y)

    def _update_cursor_tracking(self):
        self.technical_collection.cursor_tracker.position = self.app.cursor.position

    def _update_menu_animation(self):
        self.bg_collection.main_menu_title.position = Vec2(
            40 + math.sin(self.app.tick_count / 50) * 5,
            285 + math.sin(self.app.tick_count / 30) * 10
        )
        self.bg_collection.main_menu_title.rotation = math.sin(self.app.tick_count/100)*5

    def _update_fps_counter(self):
        self.technical_collection.fps_counter.text = f"{int(self.app.fps)} FPS" + f" {int(self.app.average_fps)} Averages FPS"


def start(app: Core):
    app.game = Game(app)

def update(app: Core):
    app.game.update()

app = Core(start=start, update=update,asset_path="Assets")
app.run()