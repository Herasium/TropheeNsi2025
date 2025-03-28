
import random
from HeraEngine import *

class Maze():
    def __init__(self,core:Core):
        self._core = core
        self.size = Vec2(19,49)
        self.seed = 1
        self.FREE,self.WALL,self.NORTH, self.SOUTH, self.EAST, self.WEST = True,False,'n', 's', 'e', 'w'
        random.seed(self.seed)
        self._core.log.INFO("Created MAZE.")

    def _debug_display_maze(self):
        for y in range(self.size.y):
            for x in range(self.size.x):
                    print("⬜" if self.maze[(x, y)] else "⬛", end='')
            print()

    def _setup_walls(self):
        for x in range(self.size.x):
            for y in range(self.size.y):
                self.maze[(x, y)] = self.WALL 

    def _visit(self,x,y):
        self.maze[(x, y)] = self.FREE

        while True:
                unvisitedNeighbors = []
                if y > 1 and (x, y - 2) not in self.hasVisited:
                    unvisitedNeighbors.append(self.NORTH)

                if y < self.size.y - 2 and (x, y + 2) not in self.hasVisited:
                    unvisitedNeighbors.append(self.SOUTH)

                if x > 1 and (x - 2, y) not in self.hasVisited:
                    unvisitedNeighbors.append(self.WEST)

                if x < self.size.x - 2 and (x + 2, y) not in self.hasVisited:
                    unvisitedNeighbors.append(self.EAST)

                if len(unvisitedNeighbors) == 0:
                    return
                else:
                    nextIntersection = random.choice(unvisitedNeighbors)
                    if nextIntersection == self.NORTH:
                        nextX = x
                        nextY = y - 2
                        self.maze[(x, y - 1)] = self.FREE
                    elif nextIntersection == self.SOUTH:
                        nextX = x
                        nextY = y + 2
                        self.maze[(x, y + 1)] = self.FREE 
                    elif nextIntersection == self.WEST:
                        nextX = x - 2
                        nextY = y
                        self.maze[(x - 1, y)] = self.FREE 
                    elif nextIntersection == self.EAST:
                        nextX = x + 2
                        nextY = y
                        self.maze[(x + 1, y)] = self.FREE 

                    self.hasVisited.append((nextX, nextY)) 
                    self._visit(nextX, nextY)

    def _setup_maze(self):
        self.maze = {}
        self.hasVisited = [(1, 1)]
        self._setup_walls()
        self._visit(1,1)
        self._core.log.DEBUG("Finished maze generation.")

    def _setup_map(self):
        self.offset = Vec2(0,0)
        self.map = Collection(self._core)
        self.block_size = Vec2(100,100)

        self.map.Entity("background",position = Vec2(0,0), size=Vec2(1920,1080), color =Color(0,0,0),layer=layers.background)

        self.map.Entity("torch",position = Vec2(0,0), size = Vec2(300,300), color=Color(255,214,0),layer=layers.background)

        for x in range(self.size.x):
            for y in range(self.size.y):
                if self.maze[(x, y)] :
                    self.map.Entity(f"block-{x}-{y}",size=self.block_size,position=Vec2(x*self.block_size.x,y*self.block_size.y),color=Color(0,0,0),layer=layers.background)

    def _setup_player(self):
        self.player_position = Vec2(1,1)
        self.map.Entity("player",size = Vec2(50,50),position = Vec2(125,125),color = Color(255,0,0),layer=layers.background)

    def setup(self):
        self._core.update = self.update
        self._setup_maze()
        self._setup_map()
        self._setup_player()
        self.map.Text("debug",text="Hello World",position = Vec2(0,0), size= Vec2(0,0),font=self._core.monogram,layer=layers.background)
        self._core.log.INFO("Launched MAZE.")

    def _position_maze(self):
        for x in range(self.size.x):
            for y in range(self.size.y):
                if self.maze[(x, y)] :
                    getattr(self.map,f"block-{x}-{y}").position = (Vec2(x,y) - self.offset)*self.block_size


    def _position_player(self):
        self.map.player.position = (self.player_position - self.offset) * self.block_size + (self.map.player.size / 2)
        if self.map.player.position.y > 900 and self.offset.y < 49:
            self.offset += Vec2(0,1)
            self._position_maze()
            self._position_player()

        if self.map.player.position.y < 180 and self.offset.y > 0:
            self.offset += Vec2(0,-1)
            self._position_maze()
            self._position_player()

    def _handle_key_press(self):
        for key in self._core.keyboard.last_pressed:
            if self._core.keyboard.get_key(key) == "right_arrow":
                if self.maze[(self.player_position.x + 1, self.player_position.y)] :
                    self.player_position += Vec2(1,0)
                    self._position_player()
            if self._core.keyboard.get_key(key) == "left_arrow":
                if self.maze[(self.player_position.x - 1, self.player_position.y)] :
                    self.player_position += Vec2(-1,0)
                    self._position_player()
            if self._core.keyboard.get_key(key) == "up_arrow":
                if self.maze[(self.player_position.x , self.player_position.y - 1)] :
                    self.player_position += Vec2(0,-1)
                    self._position_player()
            if self._core.keyboard.get_key(key) == "down_arrow":
                if self.maze[(self.player_position.x , self.player_position.y+ 1)] :
                    self.player_position += Vec2(0,1)
                    self._position_player()

    def update(self,_):
        self.map.torch.position = self._core.cursor.position - Vec2(150,150)
        self.map.debug.text = f"FPS: {int(self._core.fps)}:{int(self._core.average_fps)} POSITION: {self.player_position} OFFSET: {self.offset} ECOUNT: {self._core.entity_count}"
        self._handle_key_press()





