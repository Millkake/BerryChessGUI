import pygame as pg
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from utils.spritesheet import Spritesheet
from utils.standard_values import *

import json


class ChessBoard:
    def __init__(self, img_path=r'vfx\chess_board.png', SIZEX=1000, SIZEY=1000, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)):
        """
        ChessBoard class: Handles rendering + logic of the chessboard, not input
        """

        self.image = pg.image.load(img_path).convert()
        self.image = pg.transform.scale(self.image, (SIZEX, SIZEY))  # scale to fit
        self.rect = self.image.get_rect(center=center)
        self.topleft = self.rect.topleft


        # SETTINGS: wich color on top...
        self.top_color = 'black' 
        self.bottom_color = 'white' if self.top_color == 'black' else 'black'

        self.board_state = self.reload_starting_positions()

        # game handling
        self.turn = 'white'


        # saving mechanisms
        self.move_log = []  # list of (piece, old_pos, new_pos, captured_piece)


    def reload_starting_positions(self):
        self.board_state = [[None for _ in range(8)] for _ in range(8)]
        # top
        # rooks
        self.board_state[0][0], self.board_state[0][7] = Rook(PREFIX[self.top_color] + 'rook.png', self.top_color, pos=(0, 0)), Rook(PREFIX[self.top_color] + 'rook.png', self.top_color, pos=(0, 7)) 
        # Knights
        self.board_state[0][1], self.board_state[0][6] = Knight(PREFIX[self.top_color] + 'knight.png', self.top_color, pos=(0, 1)), Knight(PREFIX[self.top_color] + 'knight.png', self.top_color, pos=(0, 6))
        # Bishops
        self.board_state[0][2], self.board_state[0][5] = Bishop(PREFIX[self.top_color] + 'bishop.png', self.top_color, pos=(0, 2)), Bishop(PREFIX[self.top_color] + 'bishop.png', self.top_color, pos=(0, 5))
        # queen
        self.board_state[0][4] = Queen(PREFIX[self.top_color] + 'queen.png', self.top_color, pos=(0, 4))
        # king
        self.board_state[0][3] = King(PREFIX[self.top_color] + 'king.png', self.top_color, pos=(0, 3))

        # PAWNS
        for x in range(0, 8):
            self.board_state[1][x] = Pawn(PREFIX[self.top_color] + 'pawn.png', self.top_color, pos=(1, x))
        # bottom
        # rooks
        self.board_state[7][0], self.board_state[7][7] = Rook(PREFIX[self.bottom_color] + 'rook.png', self.bottom_color, pos=(7, 0)), Rook(PREFIX[self.bottom_color] + 'rook.png', self.bottom_color, pos=(7, 7)) 
        # Knights
        self.board_state[7][1], self.board_state[7][6] = Knight(PREFIX[self.bottom_color] + 'knight.png', self.bottom_color, pos=(7, 1)), Knight(PREFIX[self.bottom_color] + 'knight.png', self.bottom_color, pos=(7, 6))
        # Bishops
        self.board_state[7][2], self.board_state[7][5] = Bishop(PREFIX[self.bottom_color] + 'bishop.png', self.bottom_color, pos=(7, 2)), Bishop(PREFIX[self.bottom_color] + 'bishop.png', self.bottom_color, pos=(7, 5))
        # queen
        self.board_state[7][4] = Queen(PREFIX[self.bottom_color] + 'queen.png', self.bottom_color, pos=(7, 4))
        # king
        self.board_state[7][3] = King(PREFIX[self.bottom_color] + 'king.png', self.bottom_color, pos=(7, 3))

        # PAWNS
        for x in range(0, 8):
            self.board_state[6][x] = Pawn(PREFIX[self.bottom_color] + 'pawn.png', self.bottom_color, pos=(6, x))


        return self.board_state
    

    def in_bounds(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def update_move_log(self, piece, old_pos, new_pos, captured_piece):
        piece = piece.__class__.__name__ + '_' + piece.color
        captured_piece = None if captured_piece is None else captured_piece.__class__.__name__ + '_' + captured_piece.color
        self.move_log.append((piece, old_pos, new_pos, captured_piece))
    
    def update_pos(self, old_pos, new_pos):
        """
        Move piece from old_pos (row,col) to new_pos (row,col).
        Handles captures (overwrites target).
        """
        orow, ocol = old_pos
        nrow, ncol = new_pos
        piece = self.board_state[orow][ocol]
        if piece is None:
            return False

        # if move legal, perform
        # (we assume caller validated legality)
        target = self.board_state[nrow][ncol]
        # capture automatically by overwriting
        self.board_state[orow][ocol] = None
        piece.update_pos((nrow, ncol))
        self.board_state[nrow][ncol] = piece

        self.update_move_log(piece, old_pos, new_pos, target)

        return True
    
    def check_if_game_end(self):
        counter  = 0
        for row in self.board_state:
            for piece in row:
                if isinstance(piece, King):
                    counter += 1
        if counter == 2:
            return False
        return True  # no kings found, game over
        
    def save_game(self, path):
        with open(path, 'w') as f:
            json.dump(self.move_log, f)

        self.move_log = []


    def render(self, window):
        window.blit(self.image, self.rect)

        for y in range(0, 8):
            for x in range(0, 8):
                target = self.board_state[y][x]
                if target != None:
                    target.render(window, self.topleft)
                else:
                    continue

