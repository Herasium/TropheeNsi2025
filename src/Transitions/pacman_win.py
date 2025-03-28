from HeraEngine import *
from Transitions.game_over import GameOver
from Transitions.game_over_glitched import GameOverGlitched
from Transitions.dream_4_corrupted import Dream45
from Transitions.you_won import YouWon

class PacManWin:
    
    def __init__(self,map,core: Core):
        self._core = core
        self._map = map
        self._core.update = self.update
        self._core.log.INFO("Launched PACMAN Win transition. Took over the update event.")
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
                self._map.quit()
                YouWon(self._core,45)


        self.tick += 1