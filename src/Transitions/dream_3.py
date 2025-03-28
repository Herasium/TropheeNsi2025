
from HeraEngine import *
from MiniGames.puzzle import Puzzle

class Dream3:
    def __init__(self,core: Core):
        self._core = core
        self._core.update = self.update
        self.in_transition = True
        self._setup_transition()
        self._core.log.INFO("Dream 3 transition launched.")
        
    def _setup_transition(self):
        self.start_count = self._core.tick_count
        self._chaged_start = False
        self.transition_collection = Collection(self._core)
        self.transition_collection.Entity(
            "background", layer=layers.background,
            size=Vec2(1920, 1080), position=Vec2(0, 0),
            color=Color(0, 0, 0)
        )
        self.transition_collection.Entity("d",layer=layers.background,position = Vec2(825,-490),size=Vec2(30,52),texture="Assets/Textures/Transition/Dream1/D.raw")
        self.transition_collection.Entity("r",layer=layers.background,position = Vec2(857,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/Dream1/r.raw")
        self.transition_collection.Entity("e",layer=layers.background,position = Vec2(890,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/Dream1/e.raw")
        self.transition_collection.Entity("a",layer=layers.background,position = Vec2(925,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/Dream1/a.raw")
        self.transition_collection.Entity("m",layer=layers.background,position = Vec2(957,-505),size=Vec2(39,38),texture="Assets/Textures/Transition/Dream1/m.raw")
        self.transition_collection.Entity("slash",layer=layers.background,position = Vec2(1020,-490),size=Vec2(34,52),texture="Assets/Textures/Transition/Dream1/#.raw")
        self.transition_collection.Entity("one",layer=layers.background,position = Vec2(1060,-490),size=Vec2(30,52),texture="Assets/Textures/Transition/Dream1/3.raw")

        
    def update(self,_):
        if self.in_transition == True:
            self.update_transition()
        else:
            self._core.log.INFO("Launching Puzzle.")
            self._core.puzzle = Puzzle(self._core)
            self._core.puzzle.setup()

    def update_transition(self):
        elapsed_ticks = self._core.tick_count - self.start_count
        
        if elapsed_ticks <= 200:
            return
        
        transition_elements = [
            ("d", -490, 490),
            ("r", -490, 505),
            ("e", -490, 505),
            ("a", -490, 505),
            ("m", -490, 505),
            ("slash", -490, 490),
            ("one", -490, 490)
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
            