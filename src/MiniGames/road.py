import random
from HeraEngine import *

from Transitions.road_death import RoadDeathTransition
from Transitions.road_win import RoadWin

class Road():

    def __init__(self,core: Core):
        self._core = core
        self._core.next = 1
        self._core.log.INFO("Created ROAD.")
        self.invincible = False

    def _setup_map(self):
        self.move_tick = 0
        self.map = Collection(self._core)
        self.map.Entity(name="bg_0",size = Vec2(1920,1080),position=Vec2(0,0),color=Color(0,0,0),layer=layers.background)
        self.map.Entity(name="bg_1",size=Vec2(1920,1080),position=Vec2(0,0),color=Color(0,255,0),layer=layers.background,texture="Assets/Textures/Minigames/Road/grass.raw")
        self.map.Entity(name="bg_2",size=Vec2(1920,1080),position=Vec2(0,-1080),color=Color(0,255,255),layer=layers.background,texture="Assets/Textures/Minigames/Road/grass.raw")

        self.map.Entity(name="road_1",size=Vec2(480,1080),position = Vec2(720,0),color=Color(255,0,0),layer=layers.background, texture="Assets/Textures/Minigames/Road/road.raw")
        self.map.Entity(name="road_2",size=Vec2(480,1080),position = Vec2(720,-1080),color=Color(255,0,255),layer=layers.background, texture="Assets/Textures/Minigames/Road/road.raw")

    def _setup_player(self):
        self.player_position = Vec2(885,780)
        self.map.Entity(name="player",size = Vec2(150,204),position=Vec2(885,780),color = Color(255,255,255),layer=layers.background,texture="Assets/Textures/Minigames/Road/car.raw")

    def _setup_obstacles(self):
        self.obstacles = Collection(self._core)
        self.spawn_delay = 900
        self.obstacles_speed = 4
        self.new_obstacle = random.randint(int(self.spawn_delay - self.spawn_delay/10),int(self.spawn_delay + self.spawn_delay/10))
        self.obstacle_tick = 0

    def _spawn_obstacle(self):
        self.spawn_delay = int(max(self.spawn_delay-10,500)*10)/10
        self.obstacles_speed = min(7,self.obstacles_speed+0.1)
        row = random.randint(0,2)
        type = random.randint(int(min(self.score/3,10)),10) == 10
        if type and self.obstacles_speed > 6.5:
            self.obstacles.Entity(name=f"obastacle-{self._core.tick_count}",position=Vec2(160*row + 720+25,-300),size=Vec2(100,100),texture=f"Assets/Textures/Minigames/Road/obstacles/hospital/sprite_{random.randint(0,7)}.raw",layer=layers.background)
            getattr(self.obstacles,f"obastacle-{self._core.tick_count}").row = row
        else:
            self.obstacles.Entity(name=f"obastacle-{self._core.tick_count}",position=Vec2(160*row + 720+25,-300),size=Vec2(100,100),texture=f"Assets/Textures/Minigames/Road/obstacles/normal/sprite_{random.randint(0,10)}.raw",layer=layers.background)
            getattr(self.obstacles,f"obastacle-{self._core.tick_count}").row = row

    def _update_obstacles(self):

        to_remove = []

        for i in self.obstacles.entity_list:
            entity = self.obstacles.entity_list[i]

            if entity.position.y > 1200:
                to_remove.append(i)

            entity.position = entity.position + Vec2(0,int((int(self.obstacles_speed))))

        for i in to_remove:
            self.score += 1
            self.obstacles.remove(i)

        self.obstacle_tick += int(self.obstacles_speed)
        if self.obstacle_tick >= self.new_obstacle:
            self.obstacle_tick = 0
            self.new_obstacle = int(random.randint(int(self.spawn_delay - self.spawn_delay/10),int(self.spawn_delay + self.spawn_delay/10)))
            self._spawn_obstacle()


    def _update_road(self):
        self.move_tick += int((int(self.obstacles_speed)))
        d = (int(self.move_tick)) % 1080
        t = (int(self.move_tick) % 1620)/1.5

        self.map.road_1.position = Vec2(720,d)
        self.map.road_2.position = Vec2(720,-1080+d)

        self.map.bg_1.position = Vec2(0,t)
        self.map.bg_2.position = Vec2(0,-1080+t)
        
        if d < 5 and t < 5 and self.score > 40:
            self.map.road_2.color = Color(0,0,0)
            self.map.bg_2.color = Color(125,125,125)

        if d > 1075 and t > 1075 and self.score > 40:
            self.map.road_1.color = Color(0,0,125)
            self.map.bg_1.color = Color(125,0,0)

    def _handle_player_inputs(self):
        for key in self._core.keyboard.last_pressed:
            if self._core.keyboard.get_key(key) == "right_arrow":
                self.player_row += 1
                if self.player_row > 2:
                    self.player_row = 0
                self.player_position = Vec2(160*self.player_row + 720,780)

            if self._core.keyboard.get_key(key) == "left_arrow":
                self.player_row -= 1
                if self.player_row < 0:
                    self.player_row = 2
                self.player_position = Vec2(160*self.player_row + 720,780)

    def _update_player_position(self):
        self.map.player.rotation = ((self.player_position - self.map.player.position)/self.player_delay).x
        self.map.player.position += (self.player_position - self.map.player.position)/self.player_delay

    def _check_collisions(self):

        self.colided =  False
        for i in self.obstacles.entity_list:
            entity = self.obstacles.entity_list[i]
            if self.map.player.collide(entity):
                self.colided = True


    def setup(self):
        self._core.update = self.update
        self.player_position = Vec2(0,0)
        self.player_row = 1
        self.player_delay = 10
        self.colided = False
        self.score = 0

        self._setup_map()
        self._setup_player()
        self._setup_obstacles()
        self.map.Entity("debug_text",size=Vec2(0, 0), position=Vec2(-1000, -1000),layer=layers.background)
        self._core.log.INFO("Launched ROAD")  

    def update(self,_):
        self._update_road()
        self._handle_player_inputs()
        self._update_player_position()
        self._update_obstacles()
        self._check_collisions()

        if self.colided and not self.invincible:
            self.obstacles.quit()
            RoadDeathTransition(self.map,self._core)

        if self.score > 50 and (int(self.move_tick)) % 1080 < 5:
            self.obstacles.quit()
            RoadWin(self.map,self._core)



        self.map.debug_text.text = f"FPS: {int(self._core.fps)};{int(self._core.average_fps)} OBS_DELAY: {self.new_obstacle};{self.obstacle_tick} LEN_OBS: {len(self.obstacles.entity_list)} SPEED: {self.obstacles_speed} COLLISIONS: {self.colided} ECOUNT {self._core.entity_count} SCORE {self.score}"