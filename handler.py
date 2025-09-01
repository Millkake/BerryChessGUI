import pygame as pg
from utils.standard_values import *
from utils.particle import Particle
import random as rd
import time
from utils.button import Button
from boards.board import ChessBoard
from boards.pvs_board import PlayerVsSelfBoard
from boards.pvb_board import PlayerVsBotBoard
from gamereview import GameReview

GAME_MODES = ['player vs player', 'player vs self', 'player vs bot', 'look at old games', 'menu']

class Handler:
    def __init__(self, img_path, scale=[WINDOW_WIDTH, WINDOW_HEIGHT]):
        self.img = pg.image.load(img_path)
        self.img = pg.transform.scale(self.img, scale)
        self.rect = self.img.get_rect()
        
        self.current_game_mode = 'menu'

        # handle particles
        self.particle_amount_on_click = 30
        self.particles = []
        self.time_since_last_particle = time.time()
        self.interval_between_rand_particles = 1
        self.particle_amount_on_time = 8


        # buttons
        self.buttons = []
        x = 420
        y = 450
        for text in GAME_MODES:
            if text == 'menu':
                continue
            self.buttons.append(Button(color=(100,100,100), x=x, y=y, width=500, height=85, text=text, on_click=text))
            y += 100


        # handle other gamemodes
        self.pvs_board = PlayerVsSelfBoard(center=CENTERPOS)
        self.pvp_board = None
        self.pvb_board = PlayerVsBotBoard(center=CENTERPOS)
        self.game_review = GameReview(8)

    
    def generate_rand_particles(self):
        curr_time = time.time()
        if curr_time - self.time_since_last_particle < self.interval_between_rand_particles:
            x, y = rd.randint(0, WINDOW_WIDTH), rd.randint(0, WINDOW_HEIGHT)
            for _ in range(self.particle_amount_on_time):
                self.particles.append(Particle(pos=(x,y), size=rd.randint(2,5), fire_gloom=True, fire_flicker=True))
        self.time_since_last_particle = curr_time


    def update_particles_and_buttons(self, window):
        # random particle son interval
        self.generate_rand_particles()

        # particles because of clicks + output of buttons
        mx, my = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            # particles
            for _ in range(self.particle_amount_on_click):
                self.particles.append(Particle(pos=(mx, my)))

                # STATE MANAGER
            for button in self.buttons:
                if button.is_over((mx, my)):
                    output = button.on_click()
                    self.current_game_mode = output

                
        for particle in self.particles:
            if particle.size == 0:
                self.particles.remove(particle)
            particle.update()
            particle.render(window)


    def run_game_review(self, window):
        self.game_review.run_game_review_engine(window)
        

    def run_player_vs_player(self, window):
        pass


    def run_player_vs_bot(self, window):
        self.pvb_board.run_pvb_board(window)


    def run_player_vs_self(self, window):
        self.pvs_board.run_pvs_board(window)


    def run_menu(self, window):
        window.blit(self.img, self.rect)
        self.update_particles_and_buttons(window)

        for button in self.buttons:
            button.draw(window)