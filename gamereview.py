import pygame as pg
import os
from utils.button import Button
from utils.standard_values import *

PREFIX = r'saves/'
SAVE_TYPES = ['pvb_games', 'pvp_games', 'pvb_games']


class GameReview:
    def __init__(self, display_amount):
        self.main_paths = [PREFIX + i for i in SAVE_TYPES]

        self.buttons = []
        x = WINDOW_WIDTH // 2 - 400
        y = WINDOW_HEIGHT // 2 
        for text in SAVE_TYPES:
            self.buttons.append(Button(color=(100,100,100), x=x, y=y, width=500, height=75, text=text, on_click=text))
            y += 100


    def run_game_review_engine(self, window):
        for button in self.buttons:
            button.draw(window)