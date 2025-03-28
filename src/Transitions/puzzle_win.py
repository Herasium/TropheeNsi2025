from HeraEngine import *
from Transitions.you_won import YouWon

class PuzzleWin:
    
    def __init__(self,map: Collection,core: Core):
        self._core = core
        self.map = map
        self._core.update = self.update
        self._core.log.INFO("Launched PUZZLE Win transition. Took over the update event.")
        self.tick = 0

    def update(self,_):

        if self.tick < 20:
            pass
        elif self.tick < 40:
            for y in range(3):
                for x in range(3):
                    getattr(self.map,f"tile_{x}_{y}").texture = f"Assets/Textures/Minigames/Puzzle/prune/{y}_{x}.raw.corrupted"
        elif self.tick < 60:
            for y in range(3):
                for x in range(3):
                    getattr(self.map,f"tile_{x}_{y}").texture = f"Assets/Textures/Minigames/Puzzle/prune/{y}_{x}.raw"
                    
        elif self.tick < 100:
            for y in range(3):
                for x in range(3):
                    getattr(self.map,f"tile_{x}_{y}").texture = f"Assets/Textures/Minigames/Puzzle/prune/{y}_{x}.raw.corrupted"
                    
        elif self.tick < 150:
            for y in range(3):
                for x in range(3):
                    getattr(self.map,f"tile_{x}_{y}").texture = f"Assets/Textures/Minigames/Puzzle/prune/{y}_{x}.raw"
        
        elif self.tick < 200:
            for y in range(3):
                for x in range(3):
                    getattr(self.map,f"tile_{x}_{y}").texture = f"Assets/Textures/Minigames/Puzzle/prune/{y}_{x}.raw.corrupted"

        elif self.tick < 300:
            self.map.quit()
            YouWon(self._core,4)

        self.tick += 1
        