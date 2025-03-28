#Class representing the cursor and it's interactions such as movements, click and lock and show/hide.

from HeraEngine.types.Vec2 import Vec2

class Cursor():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.position = Vec2(self.x,self.y)

        self.visibility = True #true = visible
        self.on_right_click = []
        self.on_left_click = []
        self.on_middle_click = []

        self.on_move = []

        self._buffer = []

    def send_events(self,event_list):
        for i in event_list:
            i(self)

    def window_register_action(self,type,**kwargs):
        self._buffer.append([type,kwargs])

    def update(self):
        for i in self._buffer:

            type = i[0]
            kwargs = i[1]

            if type == "move":
                self.x = kwargs["x"]
                self.y = kwargs["y"]
                self.position = Vec2(self.x,self.y)

                self.send_events(self.on_move)
            if type == "rbuttondown":
                self.send_events(self.on_right_click)
            if type == "lbuttondown":
                self.send_events(self.on_left_click)

        self._buffer = []