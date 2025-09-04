import pygame as pg
from boards.board import ChessBoard
from utils.standard_values import *
from utils.utils import draw_text
import os
import sys



class PlayerVsSelfBoard(ChessBoard):
    """
    A chess board class for player-vs-self mode, allowing manual piece selection and movement.
    Args:
        img_path (str): Path to the chess board image.
        SIZEX (int): Width of the board in pixels.
        SIZEY (int): Height of the board in pixels.
        center (tuple): Center position of the board on the window.
    Attributes:
        topleft (tuple): Top-left pixel position of the board.
        current_selected (tuple or None): Currently selected cell (row, col) or None.
    Methods:
        mouse_to_cell_pos(mpos):
            Converts mouse pixel position to board cell coordinates.
        highlight_selected(window):
            Highlights the currently selected cell on the board.
        show_possible_moves(piece_pos, window):
            Displays possible moves for the selected piece.
        handle_board_click(cell_pos):
            Handles logic for selecting and moving pieces based on board clicks.
        run_pvs_board(window):
            Main loop for handling input and rendering the board in player-vs-self mode.
    """
    def __init__(self, img_path=r'vfx\chess_board.png', SIZEX=1000, SIZEY=1000, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)):
        super().__init__(img_path, SIZEX, SIZEY, center)
        self.topleft = self.rect.topleft
        self.current_selected = None


    def mouse_to_cell_pos(self, mpos):
        mx, my = mpos[0], mpos[1]
        relx, rely = mx - self.topleft[0], my - self.topleft[1]
        flatx, flaty = relx // TILE_SIZE, rely // TILE_SIZE
        
        return flaty, flatx
    
    def highlight_selected(self, window):
        if self.current_selected is None:
            return
        row, col = self.current_selected
        x = self.topleft[0] + col * TILE_SIZE
        y = self.topleft[1] + row * TILE_SIZE
        pg.draw.rect(window, HIGHLIGHT, (x, y, TILE_SIZE, TILE_SIZE), 5)

    def show_possible_moves(self, piece_pos, window):
        if piece_pos is None:
            return
        row, col = piece_pos
        piece = self.board_state[row][col]
        if piece is None:
            return
        moves = piece.moves(self.board_state)
        for (r, c) in moves:
            cx = self.topleft[0] + c * TILE_SIZE + TILE_SIZE // 2
            cy = self.topleft[1] + r * TILE_SIZE + TILE_SIZE // 2
            pg.draw.circle(window, (0, 255, 0), (cx, cy), 12)

    def handle_board_click(self, cell_pos):
        cell = cell_pos
        if cell is None:
            self.current_selected = None
            return

        row, col = cell
        targeted = self.board_state[row][col]

        if self.current_selected is None:
            # select piece if it's your turn's piece
            if targeted is not None and targeted.color == self.turn:
                self.current_selected = (row, col)
        else:
            sel_row, sel_col = self.current_selected
            sel_piece = self.board_state[sel_row][sel_col]
            # reselect your own piece
            if targeted is not None and targeted.color == self.turn:
                self.current_selected = (row, col)
                return

            # attempt move to empty or capture target
            if sel_piece is not None and (row, col) in sel_piece.moves(self.board_state):
                sel_piece.has_moved = True
                moved = self.update_pos((sel_row, sel_col), (row, col))
                if moved:
                    # flip turn
                    self.turn = 'black' if self.turn == 'white' else 'white'

            # clear selection either way
            self.current_selected = None

    def run_pvs_board(self, window):
        if self.check_if_game_end():
            draw_text(WINDOW_WIDTH//2-70, WINDOW_HEIGHT//2, 80, "Game Over!", window, color=(255,0,0))
            draw_text(WINDOW_WIDTH//2-70, WINDOW_HEIGHT//2 + 80, 70, "Press b to go back", window, color=(255,0,0))
            self.save_game(
                r'saves/pvs_games/' + 'pvs_save_' + str(len(os.listdir(r'saves/pvs_games/')) + 1) + '.json'
            )
            self.move_log = []
            pg.display.flip()
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN and event.key == pg.K_b:
                        self.board_state = self.reload_starting_positions()
                        self.__init__()
                        return
            
        mouse_pressed = pg.mouse.get_pressed()
        if mouse_pressed[0]:
            mx, my = pg.mouse.get_pos()
            row, col = self.mouse_to_cell_pos((mx, my))
            if self.in_bounds(row, col):
                self.handle_board_click((row, col))

        # --- Rendering --- #
        self.render(window)
        self.show_possible_moves(self.current_selected, window)
        self.highlight_selected(window)
        draw_text(10, 10, 30, f"Turn: {self.turn.capitalize()}", window)

        keys = pg.key.get_just_pressed()
        if keys[pg.K_s]:
            self.save_game(path=r'saves/pvs_games/' + 'pvs_save_' + str(len(os.listdir(r'saves/pvs_games/')) + 1) + '.json')

        




    