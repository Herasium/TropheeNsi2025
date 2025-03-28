
from HeraEngine import *

class GameOver:
    def __init__(self,core: Core):
        self._core = core
        self._core.update = self.update
        self.in_transition = True
        self._setup_transition()
        self._core.log.INFO("Game Over. Game over transition launched.")
        
    def _setup_transition(self):
        self.start_count = self._core.tick_count
        self._chaged_start = False
        self.transition_collection = Collection(self._core)
        self.transition_collection.Entity(
            "background", layer=layers.background,
            size=Vec2(1920, 1080), position=Vec2(0, 0),
            color=Color(0, 0, 0)
        )
        self.transition_collection.Entity("g",layer=layers.background,position = Vec2(806,-490),size=Vec2(30,52),texture="Assets/Textures/Transition/GameOver/G.raw")
        self.transition_collection.Entity("a",layer=layers.background,position = Vec2(840,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/GameOver/a.raw")
        self.transition_collection.Entity("m",layer=layers.background,position = Vec2(874,-505),size=Vec2(39,38),texture="Assets/Textures/Transition/GameOver/m.raw")
        self.transition_collection.Entity("e",layer=layers.background,position = Vec2(918,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/GameOver/e.raw")
        self.transition_collection.Entity("o",layer=layers.background,position = Vec2(964,-490),size=Vec2(30,52),texture="Assets/Textures/Transition/GameOver/O.raw")
        self.transition_collection.Entity("v",layer=layers.background,position = Vec2(998,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/GameOver/v.raw")
        self.transition_collection.Entity("second_e",layer=layers.background,position = Vec2(1032,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/GameOver/e.raw")
        self.transition_collection.Entity("r",layer=layers.background,position = Vec2(1066,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/GameOver/r.raw")
        self.transition_collection.Entity("!",layer=layers.background,position = Vec2(1100,-490),size=Vec2(12,52),texture="Assets/Textures/Transition/GameOver/!.raw")
        
        
    def update(self,_):
        if self.in_transition == True:
            self.update_transition()
        else:
            self._core.log.INFO("Re-Launching Menu.")
            self._core.game.__init__(self._core)
            self._core.update = self._core.game.update
    
    
    def update_transition(self):
        elapsed_ticks = self._core.tick_count - self.start_count
        
        if elapsed_ticks <= 200:
            return
        
        transition_elements = [
            ("g", -490, 490),
            ("a", -490, 505),
            ("m", -490, 505),
            ("e", -490, 505),
            ("o", -490, 490),
            ("v", -490, 505),
            ("second_e", -490, 505),
            ("r", -490, 505),
            ("!", -490, 490),
        ]
        
        if elapsed_ticks <= 700:
            for i, (key, start, end) in enumerate(transition_elements):
                t = (self._core.tick_count - (self.start_count + 200 + 10 * i)) / 100
                getattr(self.transition_collection,key).position = Vec2(
                    getattr(self.transition_collection,key).position.x,
                    elastic_interpolation(start, end, t)
                )
        
        elif elapsed_ticks <= 1200:
            if not self._chaged_start:
                self._chaged_start = True
                self.second_start_count = self._core.tick_count
            
            for i, (key, end, start) in enumerate(transition_elements):
                t = (self._core.tick_count - (self.second_start_count + 10 * i)) / 100
                getattr(self.transition_collection,key).position = Vec2(
                    getattr(self.transition_collection,key).position.x,
                    reverse_elastic_interpolation(start , end+ 1980, t) 
                )
        else:
            self.in_transition = False
            self.transition_collection.quit()