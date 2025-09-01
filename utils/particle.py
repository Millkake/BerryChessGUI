import pygame as pg
import random
import random, math
import pygame as pg
from utils.standard_values import BGPARTICLE_COLORS

class Particle:
    def __init__(self, pos:tuple, size:int=6, color:tuple=(53,114,183), velocity:float=1.5, fade_factor='random', fire_gloom=False, fire_flicker=False) -> None:
        self.x, self.y = pos
        self.size = size 
        self.fire_gloom = fire_gloom
        self.fire_flicker = fire_flicker

        # Generate random direction uniformly around a circle
        angle = random.uniform(0, 2 * math.pi)
        self.vec2d = (math.cos(angle) * velocity, math.sin(angle) * velocity)

        self.fade_factor = fade_factor
        if self.fade_factor == 'random':
            self.fade_factor = random.uniform(0.01, 0.5)

        # colro manipulation
        self.color = random.choice(BGPARTICLE_COLORS) if self.fire_gloom else color
        self.life_cycle = 0
        self.delta_life_cycle = 0


    def flicker_color(self):
        if self.fire_flicker:
            self.color = random.choice(BGPARTICLE_COLORS)
    
    def render(self, window):
        pg.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.size))

    def update(self):
        self.flicker_color()
        self.x += self.vec2d[0]
        self.y += self.vec2d[1]
        self.size = max(0, self.size - self.fade_factor)
        self.life_cycle += 1
