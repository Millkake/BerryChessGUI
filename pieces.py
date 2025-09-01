import pygame as pg
from utils.standard_values import *
from utils.utils import load_image



class Piece:
    def __init__(self, path, color, pos, scale=(TILE_SIZE, TILE_SIZE)):
        self.img = load_image(path, scale)
        self.color = color  # 'white' or 'black'
        # position as (row, col)
        self.pos = tuple(pos)
        self.possible_moves = []

        self.has_moved = False  # for pawns, rooks, kings (castling, initial 2-step)

    def render(self, surface, topleft):
        row, col = self.pos
        x = topleft[0] + (col * TILE_SIZE)
        y = topleft[1] + (row * TILE_SIZE)
        surface.blit(self.img, (x, y))

    def in_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def is_pos_under_attack(self, board_state, target_row, target_col):
        """
        Returns True if square (target_row, target_col) is attacked by any enemy piece.
        Must avoid recursion problems: do not call opposing King's .moves() (which can call this).
        For kings, check adjacency manually.
        """
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = board_state[r][c]
                if piece is None:
                    continue
                if piece.color == self.color:
                    continue

                # If the piece is a King, check adjacency instead of calling moves()
                if piece.__class__.__name__ == 'King':
                    for dr, dc in KING_MOVES:
                        ar, ac = r + dr, c + dc
                        if (ar, ac) == (target_row, target_col):
                            return True
                    continue

                # For pawns we want the attack squares specifically (their capture moves)
                if piece.__class__.__name__ == 'Pawn':
                    # Pawn attack squares depend on color
                    prow, pcol = piece.pos
                    direction = -1 if piece.color == 'white' else 1
                    for dc in (-1, 1):
                        ar, ac = prow + direction, pcol + dc
                        if (ar, ac) == (target_row, target_col):
                            return True
                    continue

                # For other pieces, rely on their move generation (it doesn't call is_pos_under_attack)
                # which returns the squares they can move to (i.e., attack/capture squares).
                moves = piece.moves(board_state)
                if (target_row, target_col) in moves:
                    return True

        return False

    def moves(self, board_state):
        return []

    def update_pos(self, new_pos):
        self.pos = tuple(new_pos)


class Pawn(Piece):
    def __init__(self, path, color, pos, scale=(TILE_SIZE, TILE_SIZE)):
        super().__init__(path, color, pos, scale)
        self.start_row = 6 if self.color == 'white' else 1
        self.direction = -1 if self.color == 'white' else 1

    def moves(self, board_state):
        row, col = self.pos
        self.possible_moves = []

        # forward one
        fr = row + self.direction
        if self.in_bounds(fr, col) and board_state[fr][col] is None:
            self.possible_moves.append((fr, col))

            # forward two from start
            fr2 = row + 2 * self.direction
            if row == self.start_row and self.in_bounds(fr2, col) and board_state[fr2][col] is None:
                self.possible_moves.append((fr2, col))

        # captures
        for dc in (-1, 1):
            cr, cc = row + self.direction, col + dc
            if self.in_bounds(cr, cc):
                target = board_state[cr][cc]
                if target is not None and target.color != self.color:
                    self.possible_moves.append((cr, cc))

        return self.possible_moves


class Rook(Piece):
    def moves(self, board_state):
        row, col = self.pos
        self.possible_moves = []

        # four directions (vertical/horizontal)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            for step in range(1, BOARD_SIZE):
                nr, nc = row + dr * step, col + dc * step
                if not self.in_bounds(nr, nc):
                    break
                target = board_state[nr][nc]
                if target is None:
                    self.possible_moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        self.possible_moves.append((nr, nc))
                    break

        return self.possible_moves


class Knight(Piece):
    def moves(self, board_state):
        row, col = self.pos
        self.possible_moves = []
        for dr, dc in KNIGHT_MOVES:
            nr, nc = row + dr, col + dc
            if self.in_bounds(nr, nc):
                target = board_state[nr][nc]
                if target is None or target.color != self.color:
                    self.possible_moves.append((nr, nc))
        return self.possible_moves


class Bishop(Piece):
    def moves(self, board_state):
        row, col = self.pos
        self.possible_moves = []

        for dr, dc in BISHOP_MOVES:
            for step in range(1, BOARD_SIZE):
                nr, nc = row + dr * step, col + dc * step
                if not self.in_bounds(nr, nc):
                    break
                target = board_state[nr][nc]
                if target is None:
                    self.possible_moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        self.possible_moves.append((nr, nc))
                    break
        return self.possible_moves


class Queen(Piece):
    def moves(self, board_state):
        # combine rook + bishop patterns
        row, col = self.pos
        self.possible_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] + BISHOP_MOVES
        for dr, dc in directions:
            for step in range(1, BOARD_SIZE):
                nr, nc = row + dr * step, col + dc * step
                if not self.in_bounds(nr, nc):
                    break
                target = board_state[nr][nc]
                if target is None:
                    self.possible_moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        self.possible_moves.append((nr, nc))
                    break
        return self.possible_moves


class King(Piece):

    def moves(self, board_state):
        row, col = self.pos
        self.possible_moves = []
        for dr, dc in KING_MOVES:
            nr, nc = row + dr, col + dc
            if not self.in_bounds(nr, nc):
                continue
            # can't move into square attacked by enemy
            if self.is_pos_under_attack(board_state, nr, nc):
                continue
            target = board_state[nr][nc]
            if target is None or target.color != self.color:
                self.possible_moves.append((nr, nc))

        # castling
        if not self.has_moved and not self.is_pos_under_attack(board_state, row, col):
            # kingside
            if col + 3 < BOARD_SIZE:
                rook = board_state[row][col + 3]
                if isinstance(rook, Rook) and rook.color == self.color and not rook.has_moved:
                    if (board_state[row][col + 1] is None and
                        board_state[row][col + 2] is None and
                        not self.is_pos_under_attack(board_state, row, col + 1) and
                        not self.is_pos_under_attack(board_state, row, col + 2)):
                        self.possible_moves.append((row, col + 2))
            # queenside
            if col - 4 >= 0:
                rook = board_state[row][col - 4]
                if isinstance(rook, Rook) and rook.color == self.color and not rook.has_moved:
                    if (board_state[row][col - 1] is None and
                        board_state[row][col - 2] is None and
                        board_state[row][col - 3] is None and
                        not self.is_pos_under_attack(board_state, row, col - 1) and
                        not self.is_pos_under_attack(board_state, row, col - 2)):
                        self.possible_moves.append((row, col - 2))


        return self.possible_moves