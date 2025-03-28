from math import sin, cos, floor
import random

class RenderEngine():
    def __init__(self,core):
        self.core = core
        self.window = core.window
        self.Size = self.window.Size
        self.ORIGINX = 200
        self.ORIGINY = 200
        self.cube = [(random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)) for _ in range(8)]

    def draw_line(self, x1, y1, x2, y2, value=0, max_steps=None):

        x3,y3 = x1,y1

        x1,x2,y1,y2 = floor(x1),floor(x2),floor(y1),floor(y2)

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        if max_steps is None:
            max_steps = self.Size[0] * self.Size[1]

        steps = 0
        while steps < max_steps:
            self.window.SetPixelColor(x1, y1, value)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
            steps += 1

        if steps == max_steps:
            raise RuntimeError("Line drawing exceeded maximum steps. Possible infinite loop.")
        
    def draw_3dline(self, color, a, b):
        ax, ay = a[0]+(a[2]*0.3)+self.ORIGINX, a[1]+(a[2]*0.3)+self.ORIGINY
        bx, by = b[0]+(b[2]*0.3)+self.ORIGINX, b[1]+(b[2]*0.3)+self.ORIGINY
        self.draw_line(ax, ay, bx, by,value=color)

    def draw_cube(self, color, cube):
        a, b, c, d, e, f, g, h = cube
        self.draw_3dline( color, a, b)
        self.draw_3dline( color, b, c)
        self.draw_3dline( color, c, d)
        self.draw_3dline( color, d, a)
        
        self.draw_3dline( color, e, f)
        self.draw_3dline( color, f, g)
        self.draw_3dline( color, g, h)
        self.draw_3dline( color, h, e)
        
        self.draw_3dline( color, a, e)
        self.draw_3dline( color, b, f)
        self.draw_3dline( color, c, g)
        self.draw_3dline( color, d, h)

    def rotate_3dpoint(self,p,angle,axis):
        ret = [0, 0, 0]
        cosang = cos(angle)
        sinang = sin(angle)
        ret[0] += (cosang+(1-cosang)*axis[0]*axis[0])*p[0]
        ret[0] += ((1-cosang)*axis[0]*axis[1]-axis[2]*sinang)*p[1]
        ret[0] += ((1-cosang)*axis[0]*axis[2]+axis[1]*sinang)*p[2]
        ret[1] += ((1-cosang)*axis[0]*axis[1]+axis[2]*sinang)*p[0]
        ret[1] += (cosang+(1-cosang)*axis[1]*axis[1])*p[1]
        ret[1] += ((1-cosang)*axis[1]*axis[2]-axis[0]*sinang)*p[2]
        ret[2] += ((1-cosang)*axis[0]*axis[2]-axis[1]*sinang)*p[0]
        ret[2] += ((1-cosang)*axis[1]*axis[2]+axis[0]*sinang)*p[1]
        ret[2] += (cosang+(1-cosang)*axis[2]*axis[2])*p[2]
        return ret
    
    def rotate_object(self,obj, angle, axis):
        for i in range(len(obj)):
            obj[i] = self.rotate_3dpoint(obj[i], angle, axis)
