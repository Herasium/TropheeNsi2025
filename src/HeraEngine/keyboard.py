#Class representing the keyboard and it's interactions such as movements (keyboard moves ?), click (keyboards clicks ?) and lock (lock in bro) and show/hide (invisible keyboard).

from HeraEngine.types.Vec2 import Vec2

class Keyboard():
    def __init__(self):
        self.last_key = None
        self.last_pressed = []
        self.on_press = []
        self._buffer = []
        
        self._key_codes = {
            32:"space",
            37:"left_arrow",
            38:"up_arrow",
            39:"right_arrow",
            40:"down_arrow",
            27:"echap",
            91:"windows",
        }

    def send_events(self,event_list,*args):
        for i in event_list:
            i(self,*args)

    def window_register_action(self,type,**kwargs):
        self._buffer.append([type,kwargs])

    def get_key(self,key):
        if key in self._key_codes:
            return self._key_codes[key]
        return None

    def update(self):
        for i in self._buffer:

            type = i[0]
            kwargs = i[1]

            if type == "vk_key_down":
                self.last_key = kwargs["keycode"]
                self.last_pressed.append(kwargs["keycode"])
                self.send_events(self.on_press,self.last_key)


        self._buffer = []