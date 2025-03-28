from HeraEngine import *
from Transitions.you_won import YouWon

class RoadWin:
    
    def __init__(self,map: Collection,core: Core):
        self._core = core
        self._map = map
        self._core.update = self.update
        self._core.log.INFO("Launched ROAD Win transition. Took over the update event.")
        self.tick = 0
        self._map.remove("road_2")
        self._map.Entity("hospital",size=Vec2(480,480),position=Vec2(720,-480),layer=layers.background,texture="Assets/Textures/Minigames/Road/hospital.raw")
        self._map.player.rotation = 0
        self.startpos = self._map.player.position
        self.car_texture = Texture("Assets/Textures/Minigames/Road/car.raw")
        self.amb_texture = Texture("Assets/Textures/Minigames/Road/ambulance.raw")

    def update(self,_):
        if self.tick < 120:
            for i in self._map.entity_list:
                if i != "player" and i != "bg_0":
                    entity = self._map.entity_list[i]
                    entity.position += Vec2(0,4)
        
        elif self.tick < 210:
            self._map.player.rotation -= 1
            self._map.player.position = ease_in_out(self.startpos,Vec2(858,480),(self.tick-120)/90)

        elif self.tick < 240:
            self._map.player.size = Vec2(192,256)
            self._map.player.texture = self.amb_texture
        elif self.tick < 260:
            self._map.player.size = Vec2(150,204)
            self._map.player.texture = self.car_texture
        elif self.tick < 280:
            self._map.player.size = Vec2(192,256)
            self._map.player.texture = self.amb_texture
        elif self.tick < 300:
            self._map.player.size = Vec2(150,204)
            self._map.player.texture = self.car_texture
        elif self.tick < 320:
            self._map.player.size = Vec2(192,256)
            self._map.player.texture = self.amb_texture
        elif self.tick < 340:
            self._map.player.size = Vec2(150,204)
            self._map.player.texture = self.car_texture
        elif self.tick < 420:
            self._map.player.size = Vec2(192,256)
            self._map.player.texture = self.amb_texture
        else:
            self._map.quit()
            YouWon(self._core,3)

        self.tick += 1
        