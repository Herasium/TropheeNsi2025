import numpy as np
import random
from HeraEngine import *
from Transitions.puzzle_win import PuzzleWin

class Puzzle():
    
    def __init__(self,core: Core):
        self.core = core
        self.core.update = self.update
        self.tile_size = Vec2(360,360)
        self.saves = {"1":[[2,3,6],[1,5,9],[4,0,7]],"2":[[4,2,1],[3,5,6],[7,0,9]],"3":[[9,7,4],[3,1,6],[2,0,5]],"4":[[1,2,3],[4,5,6],[7,9,0]]}
        self.level = 1
        self.check_sorted_matrix = lambda matrix: (filtered := [num for row in matrix for num in row if num != 0]) == sorted(filtered)
        self.core.next = 3
        
    def _generate_matrix(self):
        if str(self.level) in self.saves:
            matrix = np.array(self.saves[str(self.level)])
        else:
            matrix = np.arange(1, 10).reshape(3, 3) 
            #matrix = np.random.permutation(matrix.flatten()).reshape(3, 3)  
            matrix[2, 1] = 0
        self.matrix = matrix

        
    def _setup_map(self):
        
        self._generate_matrix()
        
        self.map = Collection(self.core)
        self.map.Entity(f"back",size=Vec2(1920,1080),position=Vec2(0,0),color=Color(0,0,0),layer=layers.background)
        self.map.Entity(f"cursor",size=Vec2(0,0),position=Vec2(0,0),color=Color(0,0,0),layer=layers.background)
        self.map.Text(f"lvl_display",size=Vec2(0,0),position = Vec2(1600,20), font=self.core.monogram_big,text="Level 0",layer=layers.background)
        self.map.Text(f"count_display",size=Vec2(0,0),position = Vec2(1600,50), font=self.core.monogram_big,text="Moves 0",layer=layers.background)
        self.map.Text(f"skip",size=Vec2(0,0),position = Vec2(1600,-80), font=self.core.monogram_big,text="Skip",layer=layers.background)
        self.map.cursor.hitbox.size = Vec2(1, 1)
        self.blank = Vec2(1,2)
        
        self.texture_list = []
        self.folders = ["sunny","road","pac","prune"]
        

        for y in range(3):
            for x in range(3):
                self.map.Entity(f"tile_{x}_{y}",size=self.tile_size,position=Vec2(self.tile_size.x*x+420,self.tile_size.y*y),color=Color(255,255,255),layer=layers.background)
                self.texture_list.append(Texture(f"Assets/Textures/Minigames/Puzzle/{self.folders[self.level-1]}/{y}_{x}.raw",self.core))
                getattr(self.map,f"tile_{x}_{y}").index = Vec2(x,y)
                    
                    
    def _has_neighbor(self,pos):
        rows, cols = len(self.matrix), len(self.matrix[0]) 
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        for dy, dx in directions:
            ny, nx = pos.y + dy,  pos.x + dx
            if 0 <= ny < rows and 0 <= nx < cols and self.matrix[ny][nx] == 0:
                return True
        
        return False
    
    def _switch(self,pos):
        value = self.matrix[pos.y,pos.x]
        position = tuple(np.argwhere(self.matrix == 0)[0])
   
        self.matrix[position[0],position[1]] = value
        self.matrix[pos.y,pos.x] = 0

                    
    def _update_textures(self):
        for x in range(3):
            for y in range(3): 
                if self.matrix[y,x] != 0:
                    texture = self.texture_list[self.matrix[y,x]-1] 
                    getattr(self.map,f"tile_{x}_{y}").texture = texture
                else:
                    getattr(self.map,f"tile_{x}_{y}").textured = False
                    
    def _check_order(self):
        return tuple(np.argwhere(self.matrix == 0)[0]) == (2,1) and self.check_sorted_matrix(self.matrix) #Check that the zero is back where it should be and that the matrix is sorted.

    def _win(self):
        if self.level < 4:
                
            self.map.quit()
            self.level += 1
            self._setup_map()
            self.move_count = 0
        else:
            PuzzleWin(self.map,self.core)
    
    def setup(self):
        self.move_count = 0
        self._setup_map()
        self.core.cursor.on_left_click.append(self._check_collisions)
        self.core.cursor.on_right_click.append(self._check_collisions)
        
    def _check_collisions(self,*args):
        for i in self.map.entity_list:
            entity = self.map.entity_list[i]
            
            if getattr(entity,"index",None) != None:  
                if self.map.cursor.collide(entity):
                    if self._has_neighbor(entity.index):
                        self._switch(entity.index)
                        self.move_count += 1
                        if self._check_order():
                            self._win()
            if i == "skip":
                if self.map.cursor.collide(entity):
                    self._win()
                
                        
        
    def update(self,_):
        self._update_textures()
        self.map.lvl_display.text = f"Level {self.level-1}"
        self.map.count_display.text = f"Moves {self.move_count}"
        self.map.cursor.position = self.core.cursor.position
        
        if self.move_count > 100:
            self.map.skip.position = Vec2(1600,80)
            
