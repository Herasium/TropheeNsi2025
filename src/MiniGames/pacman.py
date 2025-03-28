from HeraEngine import *
import numpy as np
import random

from Transitions.pacman_death import PacManDeathTransition
from Transitions.pacman_win import PacManWin


class PacMan():

    def __init__(self,core:Core):
        self._core = core
        self._tile_size = Vec2(20,20)
        self._collision_map_texture = Texture("Assets/Textures/Minigames/PacMan/collision_map.raw",self._core)

    def _debug_collisions(self):
        self.debug_map = Collection(self._core)

        for y in range(self._path_grid_x.shape[1]):
            for x in range(self._path_grid_x.shape[0]):
                value = self._get_path_tile(Vec2(x,y))
                if value != False:
                    self.debug_map.Entity(f"debug-{y}-{x}",size=Vec2(10,10),position =value * 10 + Vec2(600,0),color = Color(100,100),layer=layers.background)
    
    def _get_tile(self,position):
        rows, cols = self._collision_map_texture.data.shape

        if  0 <= position.x < cols and 0 <= position.y < rows: 
            return self._collision_map_texture.data[position.y,position.x] == 0
        return False
    
    def _setup_map(self):
        self.map = Collection(self._core)
        self.map.Entity(name="bg_0",size = Vec2(1920,1080),position=Vec2(0,0),color=Color(0,0,0),layer=layers.background)
        self.map.Entity("map_bg",size=Vec2(720,1080),position = Vec2(600,0),texture="Assets/Textures/Minigames/PacMan/map_big.raw", layer=layers.background)

    def _setup_player(self):
        self.map.Entity("player",size=Vec2(20,20),position =Vec2(610,10),color=Color(255,0,0),layer=layers.background,texture="Assets/Textures/Minigames/PacMan/pac_open_right.raw")
        self.player_position = Vec2(1,1)
        self.player_screen_position = Vec2(610,10)
        self.player_target = Vec2(610,10)
        self.player_rotation = 1
        self.player_delay = 15
        self.target_rotation = 1

    def _setup_ghosts(self):
         self.ghosts_position = {"a":Vec2(35,43),"b":Vec2(35,43),"c":Vec2(35,43),"d":Vec2(35,43)}
         self.ghost_last_direction = {"a":1,"b":2,"c":3,"d":4}
         self.ghosts = Collection(self._core)   
         self.ghosts.Entity("a",size=Vec2(20,20),position=Vec2(870,530),color=Color(255,0,255),layer=layers.background,texture="Assets/Textures/Minigames/PacMan/ghost_a_1.raw")
         self.ghosts.Entity("b",size=Vec2(20,20),position=Vec2(920,530),color=Color(255,0,0),layer=layers.background,texture="Assets/Textures/Minigames/PacMan/ghost_b_1.raw")
         self.ghosts.Entity("c",size=Vec2(20,20),position=Vec2(980,530),color=Color(0,255,0),layer=layers.background,texture="Assets/Textures/Minigames/PacMan/ghost_c_1.raw")
         self.ghosts.Entity("d",size=Vec2(20,20),position=Vec2(1030,530),color=Color(0,0,255),layer=layers.background,texture="Assets/Textures/Minigames/PacMan/ghost_d_1.raw")
         self.ghosts_textures_1 = {"a":Texture("Assets/Textures/Minigames/PacMan/ghost_a_1.raw",self._core),
                                 "b":Texture("Assets/Textures/Minigames/PacMan/ghost_b_1.raw",self._core),
                                 "c":Texture("Assets/Textures/Minigames/PacMan/ghost_c_1.raw",self._core),
                                 "d":Texture("Assets/Textures/Minigames/PacMan/ghost_d_1.raw",self._core)}
         
         self.ghosts_textures_2 = {"a":Texture("Assets/Textures/Minigames/PacMan/ghost_a_2.raw",self._core),
                                 "b":Texture("Assets/Textures/Minigames/PacMan/ghost_b_2.raw",self._core),
                                 "c":Texture("Assets/Textures/Minigames/PacMan/ghost_c_2.raw",self._core),
                                 "d":Texture("Assets/Textures/Minigames/PacMan/ghost_d_2.raw",self._core)}

    def _get_pac_texture(self):
        value = "open" if (self._core.tick_count//24) % 2 == 0 else "close"
        return f"Assets/Textures/Minigames/PacMan/pac_{value}_{self.player_rotation}.raw"

    def _get_vector(self,rotation):
        if rotation == 1:
            return Vec2(1,0)
        if rotation == 2:
            return Vec2(0,1)
        if rotation == 3:
            return Vec2(-1,0)
                
        return Vec2(0,-1)
    
    def _get_rotation(self,vector):
        if vector ==  Vec2(1,0):
            return 1
        if vector == Vec2(0,1):
            return 2
        if vector == Vec2(-1,0):
            return 3
                
        return 4

    def _moves_ghosts(self):

        possibilities_a = self._get_move_posibilities(self.ghosts_position["a"])
        direction_a = 1
        if self.ghost_last_direction["a"] in possibilities_a and len(possibilities_a) == 2:
            direction_a = self.ghost_last_direction["a"]
        else:
            direction_a = random.choice(possibilities_a)
        
        self.ghost_last_direction["a"] = direction_a
        self.ghosts_position["a"] += self._get_vector(direction_a)
        self.ghosts.a.position = self._get_path_tile(self.ghosts_position["a"]) * 10 + Vec2(600, 0)

        possibilities_b = self._get_move_posibilities(self.ghosts_position["b"])
        direction_b = 1
        if self.ghost_last_direction["b"] in possibilities_b and len(possibilities_b) == 2:
            direction_b = self.ghost_last_direction["b"]
        else:
            direction_b = random.choice(possibilities_b)
        
        self.ghost_last_direction["b"] = direction_b
        self.ghosts_position["b"] += self._get_vector(direction_b)
        self.ghosts.b.position = self._get_path_tile(self.ghosts_position["b"]) * 10 + Vec2(600, 0)

        possibilities_c = self._get_move_posibilities(self.ghosts_position["c"])
        direction_c = 1
        if self.ghost_last_direction["c"] in possibilities_c and len(possibilities_c) == 2:
            direction_c = self.ghost_last_direction["c"]
        else:
            direction_c = random.choice(possibilities_c)
        
        self.ghost_last_direction["c"] = direction_c
        self.ghosts_position["c"] += self._get_vector(direction_c)
        self.ghosts.c.position = self._get_path_tile(self.ghosts_position["c"]) * 10 + Vec2(600, 0)

        possibilities_d = self._get_move_posibilities(self.ghosts_position["d"])
        direction_d = 1
        if self.ghost_last_direction["d"] in possibilities_d and len(possibilities_d) == 2:
            direction_d = self.ghost_last_direction["d"]
        else:
            direction_d = random.choice(possibilities_d)
        
        self.ghost_last_direction["d"] = direction_d
        self.ghosts_position["d"] += self._get_vector(direction_d)
        self.ghosts.d.position = self._get_path_tile(self.ghosts_position["d"]) * 10 + Vec2(600, 0)

        if (self._core.tick_count//16) % 2 == 0:
            self.ghosts.a.texture = self.ghosts_textures_1["a"]
            self.ghosts.b.texture = self.ghosts_textures_1["b"]
            self.ghosts.c.texture = self.ghosts_textures_1["c"]
            self.ghosts.d.texture = self.ghosts_textures_1["d"]

        else:
            self.ghosts.a.texture = self.ghosts_textures_2["a"]
            self.ghosts.b.texture = self.ghosts_textures_2["b"]
            self.ghosts.c.texture = self.ghosts_textures_2["c"]
            self.ghosts.d.texture = self.ghosts_textures_2["d"]

        for i in self.ghosts.entity_list:
            entity = self.ghosts.entity_list[i]

            if self.map.player.collide(entity):
                self.coin.quit()
                self.ghosts.quit()
                PacManDeathTransition(self.map,self._core)
                break

    def _setup_coins(self):
        self.coin = Collection(self._core)
        for y in range(self._path_grid_x.shape[0]):
            for x in range(self._path_grid_x.shape[1]):
                value = self._get_path_tile(Vec2(x,y))
                if value.x != -1 and value.y != -1 and value.x * value.y % 8== 0:
                    self.countdown += 1
                    self.coin.Entity(f"coin-{y}-{x}",size=Vec2(10,10),position =value * 10 + Vec2(605,5),color = Color(255,215,0),layer=layers.background)
    

    def _handle_coins(self):

        to_remove = []

        for i in self.coin.entity_list:
            entity = self.coin.entity_list[i]

            if self.map.player.collide(entity):
                to_remove.append(i)

        for i in to_remove:
            self.coin.remove(i)
            self.countdown -= 1

    def _position_player(self):
        self.map.player.position = self.player_screen_position
        self.player_screen_position = self.player_target 

    def _can_go(self):
        if self.target_rotation == 1:
            next_tile = self._get_path_tile(self.player_position + Vec2(1,0))
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False

        if self.target_rotation == 2:
            vector = Vec2(0,1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False

        if self.target_rotation == 3:
            vector = Vec2(-1,0)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False

        if self.target_rotation == 4:
            vector = Vec2(0,-1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False
        
    def _get_move_posibilities(self,pos):
            possiblities = []

            next_tile = self._get_path_tile(pos + Vec2(1,0))
            if next_tile.x != -1 and next_tile.y != -1:
                possiblities.append(1)


            vector = Vec2(0,1)
            next_tile = self._get_path_tile(pos + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                possiblities.append(2)


            vector = Vec2(-1,0)
            next_tile = self._get_path_tile(pos + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                possiblities.append(3)

            vector = Vec2(0,-1)
            next_tile = self._get_path_tile(pos + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                possiblities.append(4)

            return possiblities
    


    def _move_player(self):
        if self.player_rotation == 1:
            next_tile = self._get_path_tile(self.player_position + Vec2(1,0))
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + Vec2(1,0)) * 10 + Vec2(600,0)
                self.player_position += Vec2(1,0)
        if self.player_rotation == 2:
            vector = Vec2(0,1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + vector) * 10 + Vec2(600,0)
                self.player_position += vector

        if self.player_rotation == 3:
            vector = Vec2(-1,0)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + vector) * 10 + Vec2(600,0)
                self.player_position += vector

        if self.player_rotation == 4:
            vector = Vec2(0,-1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + vector) * 10 + Vec2(600,0)
                self.player_position += vector

        self.map.player.texture = Texture(self._get_pac_texture(),self._core)

    def _handle_player_inputs(self):
        for key in self._core.keyboard.last_pressed:
            if self._core.keyboard.get_key(key) == "right_arrow":
                self.target_rotation = 1

            if self._core.keyboard.get_key(key) == "left_arrow":
                self.target_rotation = 3
                
            if self._core.keyboard.get_key(key) == "up_arrow":
                self.target_rotation = 4

            if self._core.keyboard.get_key(key) == "down_arrow":
                self.target_rotation = 2

        if self._can_go():
            self.player_rotation = self.target_rotation

    def _setup_path_grid(self):
        self._path_grid_x,self._path_grid_y = np.array(CSV().read("Assets/Textures/Minigames/Pacman/collisions.txt"))
        self._path_grid_x = self._path_grid_x.reshape(108,72)
        self._path_grid_y = self._path_grid_y.reshape(108,72)

    def _get_path_tile(self, position):
        if 0 <= position.x < self._path_grid_x.shape[1] and 0 <= position.y < self._path_grid_y.shape[0]:
            return Vec2(self._path_grid_x[position.y, position.x], self._path_grid_y[position.y, position.x])
        return Vec2(-1, -1)

    def setup(self):
        self.countdown = 0
        self._setup_map()
        self._setup_player()
        self._setup_path_grid()
        self._setup_coins()
        self._setup_ghosts()
        self.map.Entity("debug_text",size=Vec2(0, 0), position=Vec2(-1000, -1000),layer=layers.background)
        self._core.update = self.update
        self._core.Pipeline.clear_buffer()
        self._core.next = 4

    def update(self,_):
        self._position_player()
        if self._core.tick_count % int(self._core.average_fps / 20) == 0:
            self._move_player()

        if self._core.tick_count % int(self._core.average_fps / 10) == 0:
            self._moves_ghosts()

        self._handle_player_inputs()
        self._handle_coins()
        if self.countdown <= 0:
            self.ghosts.quit()
            self.coin.quit()
            PacManWin(self.map,self._core)
        self.map.debug_text.text = f"FPS: {int(self._core.fps)};{int(self._core.average_fps)} ECOUNT {self._core.entity_count} POSITION {self.player_position} COUNTDOWN {self.countdown}"