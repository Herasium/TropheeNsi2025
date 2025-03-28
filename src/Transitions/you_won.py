
from HeraEngine import *

class YouWon:
    def __init__(self,core: Core,next = 0):
        self._core = core
        self.next = next
        self._core.update = self.update
        self.in_transition = True
        self._setup_transition()
        self._core.log.INFO("You won. You won transition launched.")
        
    def _setup_transition(self):
        self.start_count = self._core.tick_count
        self._chaged_start = False
        self.transition_collection = Collection(self._core)
        self.transition_collection.Entity(
            "background", layer=layers.background,
            size=Vec2(1920, 1080), position=Vec2(0, 0),
            color=Color(0, 0, 0)
        )
        self.transition_collection.Entity("y",layer=layers.background,position = Vec2(844,-490),size=Vec2(30,52),texture="Assets/Textures/Transition/YouWon/Y.raw")
        self.transition_collection.Entity("o",layer=layers.background,position = Vec2(877,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/YouWon/o.raw")
        self.transition_collection.Entity("u",layer=layers.background,position = Vec2(910,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/YouWon/u.raw")
        self.transition_collection.Entity("w",layer=layers.background,position = Vec2(954,-505),size=Vec2(39,52),texture="Assets/Textures/Transition/YouWon/W.raw")
        self.transition_collection.Entity("second_o",layer=layers.background,position = Vec2(996,-490),size=Vec2(30,38),texture="Assets/Textures/Transition/YouWon/o.raw")
        self.transition_collection.Entity("n",layer=layers.background,position = Vec2(1027,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/YouWon/n.raw")
        self.transition_collection.Entity("!",layer=layers.background,position = Vec2(1062,-490),size=Vec2(12,52),texture="Assets/Textures/Transition/YouWon/!.raw")
        
        
    def update(self,_):
        if self.in_transition == True:
            self.update_transition()
        else:

            self._core.to_dream = self.next
            self._core.log.INFO("Re-Launching Menu.")
            self._core.update = self._core.game.update
            self._core.game.__init__(self._core)
            
 

    
    
    def update_transition(self):
        elapsed_ticks = self._core.tick_count - self.start_count
        
        if elapsed_ticks <= 200:
            return
        
        transition_elements = [
            ("y", -490, 490),
            ("o", -490, 505),
            ("u", -490, 505),
            ("w", -490, 490),
            ("second_o", -490, 505),
            ("n", -490, 505),
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