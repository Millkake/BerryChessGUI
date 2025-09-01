from utils.spritesheet import Spritesheet

# main.py
WINDOW_HEIGHT = 1200
WINDOW_WIDTH = 1600
FPS = 60

CENTERPOS = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]

# pieces.py
TILE_SIZE = 125
BOARD_SIZE = 8
# Movement deltas
KNIGHT_MOVES = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
KING_MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
# bishop directions as (dr, dc)
BISHOP_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50, 180)
HIGHLIGHT = (255, 45, 125)
# IMAGES- paths

PIECE_NAMES = ['bishop', 'king', 'queen', 'rook', 'pawn', 'knight']
PREFIX = { 
    'white': r'vfx\pieces\white-',
    'black': r'vfx\pieces\black-'}
SUFFIX = '.png'

# particle 
BGPARTICLE_COLORS = [
    (139, 0, 0),      # Dark Red
    (178, 34, 34),    # Firebrick
    (220, 20, 60),    # Crimson
    (255, 69, 0),     # Red-Orange
    (255, 80, 20),    # Ember Red
    (255, 100, 0),    # Deep Orange
    (255, 120, 40),   # Flame Orange
    (255, 140, 0),    # Dark Orange
    (255, 165, 0),    # Orange
    (255, 180, 80),   # Warm Yellow-Orange
    (255, 200, 50),   # Bright Yellow-Orange
    (255, 215, 0),    # Gold/Yellow
    (255, 255, 102)   # Soft Yellow
]

SAVE_PATHS = [
    'saves/pvs_games/',
    'saves/pvb_games/',
    'saves/pvp_games/'
    ]

