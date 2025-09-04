import pygame as pg
import os
from utils.button import Button
from utils.standard_values import *
import json


PREFIX = r'saves/'
SAVE_TYPES = ['pvb_games', 'pvp_games', 'pvs_games']

class Preview:
    def __init__(self, path, x, y, interval_speed=5):
        with open(path, 'r') as f:
            self.data = json.load(f)

        self.img = pg.image.load(r'vfx/chess_board.png')
        self.img = pg.transform.scale(self.img, (250,250))
        self.x = x
        self.y = y

        self.rect = self.img.get_rect(topleft=(self.x, self.y))

        self.interval_speed = interval_speed
        
        self.interval_timer = 10

        self.game_len = len(self.data)

        self.pieces = []


    def update_img_for_game(self, indx):
        for move in self.data: # (piece, old_pos, new_pos, captured_piece)
            yield move

    def render(self, window):
        window.blit(self.img, self.rect)
        self.interval_timer -= 1



    

        



class PreviewMenu:
    def __init__(self, type: str, preview_amount=9, paddingx=150, paddingytop=250, paddingybottom=125):
        self.path = r'saves/' + type 

        self.preview_amount = preview_amount

        self.y_top = paddingytop
        self.y_bottom = WINDOW_HEIGHT - paddingybottom
        self.dy = self.y_bottom - self.y_top
        self.x_left = paddingx
        self.x_right = WINDOW_WIDTH - paddingx
        self.dx = self.x_right - self.x_left

        self.dist_y = self.dy // preview_amount**0.5
        self.dist_x = self.dx // preview_amount**0.5

        self.previews = []
        self.prev_coords = []

        self.generate_coords()
        self.generate_previews(self.path)

    def generate_coords(self):
        for y in range(int(self.preview_amount**0.5)):
            for x in range(int(self.preview_amount**0.5)):
                self.prev_coords.append((self.x_left + x*self.dist_x, self.y_top + y*self.dist_y))
            

    def generate_previews(self, path):
        paths = os.listdir(path)
        indx = 0
        for coord in self.prev_coords:
            if indx >= len(paths):
                break
            self.previews.append(Preview(path + '/' + paths[indx], coord[0], coord[1]))
            indx += 1


    def run(self, window):
        for preview in self.previews:
            preview.render(window)

        


class GameReview:
    def __init__(self, display_amount):
        self.main_paths = [PREFIX + i for i in SAVE_TYPES]

        self.buttons = []
        x = WINDOW_WIDTH // 2 - 400
        y = WINDOW_HEIGHT // 2 
        for text in SAVE_TYPES:
            self.buttons.append(Button(color=(100,100,100), x=x, y=y, width=500, height=75, text=text, on_click=text))
            y += 100


        self.type = 'saves'
        self.preview_menu = None



    def run_game_review_engine(self, window):
        if self.type != 'saves':
            self.preview_menu = PreviewMenu(self.type)
            self.preview_menu.run(window)
            keys = pg.key.get_pressed()

            if keys[pg.K_r]:
                self.type = 'saves'

        elif self.type == 'saves':
            self.preview_menu = None
            for button in self.buttons:
                button.draw(window)

            if pg.mouse.get_pressed()[0]:
                mx, my = pg.mouse.get_pos()
                for button in self.buttons:
                    if button.is_over((mx, my)):
                        output = button.on_click()
                        self.type = output
        