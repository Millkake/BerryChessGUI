import pygame as pg
from sys import exit
import os
from utils.standard_values import *
from handler import Handler
from utils.utils import draw_text


pg.init()


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=True)
        self.clock = pg.Clock()
        pg.display.set_caption('Berry Chess - Alpha V0.1.2')
        pg.display.set_icon(pg.image.load(r'vfx/pieces/black-queen.png'))  

        self.handler = Handler('vfx/abstract_menu.png')

        # handling saves
        for path in SAVE_PATHS:
            os.makedirs(path, exist_ok=True)
        

    def run_handler_state_manager(self, window):
        # ['player vs player', 'player vs self', 'player vs bot', 'look at old games', 'menu']
        curr_gm = self.handler.current_game_mode
        draw_text(x=0, y=50, size=30, text=curr_gm, WINDOW=window, color=(255,255,80))
        if curr_gm == 'menu':
            self.handler.run_menu(window)
        elif curr_gm == 'player vs player':
            self.handler.run_player_vs_player(window)
        elif curr_gm == 'player vs self':
            self.handler.run_player_vs_self(window)
        elif curr_gm == 'player vs bot':
            self.handler.run_player_vs_bot(window)
        elif curr_gm == 'look at old games':
            self.handler.run_game_review(window)
        else:
            draw_text(x=0, y=50, size=30, text='Whoops ERROR! You dont have a valid handler.current_game_mode', WINDOW=window, color=(255,255,80))
        
    
    
    
    def main_loop(self):
        while True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_b:
                    self.handler.current_game_mode = 'menu'

            self.window.fill((30, 30, 30))
            

            self.run_handler_state_manager(self.window) 
            draw_text(x=0, y=0, size=30, text='fps' + str(self.clock.get_fps()), WINDOW=self.window, color=(100,100,100))
            
            
             # draw board
            pg.display.flip()



if __name__ == '__main__':
    game = Game()
    game.main_loop()
