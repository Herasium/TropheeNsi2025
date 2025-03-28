from HeraEngine import *
from Transitions.game_over import GameOver
from Transitions.game_over_glitched import GameOverGlitched

class PacManDeathTransition:
    
    def __init__(self,map,core: Core,glitched=False):
        self._core = core
        self.glitched = glitched
        self._map = map
        self._core.update = self.update
        self._core.log.INFO("Launched PACMAN Death transition. Took over the update event.")
        self.tick = 0
        self.player_pos = self._map.player.position



    def update(self,_):
        if self.tick < 40:
                pass
        elif self.tick < 80:
                self._map.player.position = Vec2(-1000,-1000)
        elif self.tick < 120:
                self._map.player.position = self.player_pos
        elif self.tick < 160:
                self._map.player.position = Vec2(-1000,-1000)
        elif self.tick < 200:
                self._map.player.position = self.player_pos
        elif self.tick < 240:
                self._map.player.position = Vec2(-1000,-1000)
        elif self.tick < 280:
                self._map.player.position = self.player_pos
        elif self.tick < 320:
                self._map.player.position = Vec2(-1000,-1000)
        elif self.tick >= 360:
                if self.glitched:
                        self._map.quit()
                        GameOverGlitched(self._core,0)
                else:
                        self._map.quit()
                        GameOver(self._core)

        self.tick += 1