import pygame as pg
from utils.standard_values import *


def draw_text(x, y, size, text, WINDOW, color=(255,255,255)):
    font = pg.font.Font(None, size)
    instructions_surface = font.render(text, True, color)
    instructions_rect = instructions_surface.get_rect(topleft=(x, y))
    WINDOW.blit(instructions_surface, instructions_rect)


def load_image(path, scale=(TILE_SIZE, TILE_SIZE)):
    try:
        img = pg.image.load(path).convert_alpha()
        img = pg.transform.smoothscale(img, scale)
        return img
    except Exception as e:
        # If image missing, create a simple placeholder surface
        surf = pg.Surface(scale, pg.SRCALPHA)
        surf.fill((200, 200, 200))
        pg.draw.line(surf, (120, 120, 120), (0, 0), (scale[0], scale[1]), 3)
        pg.draw.line(surf, (120, 120, 120), (scale[0], 0), (0, scale[1]), 3)
        return surf