from math import pi, sin, cos
from HeraEngine import *

from Transitions.game_over_glitched import GameOverGlitched

class HeartStop():
    def __init__(self,core:Core,corrupted = False):
        self.core = core
        self.corrupted = corrupted
        self.bar = Collection(self.core)
        self.bar.Entity("back",size=Vec2(1920,1080),position=Vec2(0,0),layer=layers.background,color=Color(0,0,0))
        for x in range(960):
            self.bar.Entity(f"b{x}",size=Vec2(2,10),position = Vec2(x*2,600),color=Color(57,255,20),layer=layers.background)
            
        self.tick = 1
        self.count = 0
            
        self.core.update = self.update
            
    def simulated_ecg(self,t: float, pulse_duration: float = 0.3, pause_duration: float = 0.7):
        cycle_length = pulse_duration + pause_duration
        time_in_cycle = t % cycle_length

        if time_in_cycle < pulse_duration:
            norm_time = time_in_cycle / pulse_duration
            theta = 2 * pi * norm_time
            phase = 2.0 * cos(theta)
            r_wave = -sin(theta + phase)
            q_scalar = 0.50 - 0.75 * sin(theta - 1.0)
            s_scalar = 0.25 - 0.125 * sin(1.25 * phase - 1.0)
            return 3.14 * q_scalar * r_wave * s_scalar + 0.4
        else:
            return 0
        
    def update(self,_):
        if self.count < 3:
            self.current = self.tick % 960
            
            if self.current == 480:
                self.count += 1
                
            if self.count <= 1:
                getattr(self.bar,f"b{self.current}").position = Vec2(self.current*2,(0-self.simulated_ecg(self.tick/50,4,4)*300)+600)
            else:
                getattr(self.bar,f"b{self.current}").position = Vec2(self.current*2,(0-self.simulated_ecg(self.tick/50,0,4)*300)+600)

        else:
            self.current = self.tick % 960
            getattr(self.bar,f"b{self.current}").position = Vec2(-100,-100)
            if self.current == 480:
                self.bar.quit()
                GameOverGlitched(self.core,0,self.corrupted)
            
        self.tick += 1