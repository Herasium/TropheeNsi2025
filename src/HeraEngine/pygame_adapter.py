import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading
import numpy as np
from HeraEngine.types.Vec2 import Vec2

class Window():
    def __init__(self, core,Size,cursor,keyboard):

        self.core = core
        self.cursor = cursor
        self.keyboard = keyboard

        self.Title = "Default Window"
        self.Size = Size
        self.past_size = None
        self.ready = False
        self.running = False

        self.screen = None
        self.clock = None
        self.buffer = None

    def hex_to_rgb(self, hex_color):
        return ((hex_color >> 16) & 0xFF, (hex_color >> 8) & 0xFF, hex_color & 0xFF)

    def SetPixelColor(self, x, y, color):
        if self.ready:
            rgb_color = self.hex_to_rgb(color)
            if  x < self.Size.x and y < self.Size.y:
                self.buffer[x, y] = rgb_color 

    def SetWindowSize(self, Size):
        if not isinstance(Size,Vec2):
            raise TypeError("Window size must be a Vec2")
        self.Size = Size



    def clear_buffer(self):
        if self.ready:
            self.buffer.fill(0x000000)


    def update(self):
        if self.ready:
            buffer_np = np.frombuffer(self.buffer, dtype=np.uint32).reshape(self.Size.y, self.Size.x)
            pygame.surfarray.blit_array(self.screen, buffer_np)
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def keep_alive(self):
        self.running = True
        while self.running:
            self.handle_events()

        pygame.quit()

    def MainWin(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.Size.y, self.Size.x))
        pygame.display.set_caption(self.Title)
        self.clock = pygame.time.Clock()

        self.buffer = pygame.surfarray.array3d(self.screen)  # Create a 3D array for the buffer
        self.clear_buffer()
        self.ready = True

        self.keep_alive()
        return 0

    def GetFullscreenSize(self):
            return (1920, 1080)