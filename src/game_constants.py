from pathlib import Path

FPS = 240
TILE_DRAW_DELAY = 10 # This many tiles per second get displayed one by one when the puzzle is shuffled.
SLIDE_DURATION_PLAYER = 0.2 # This many seconds to finish the sliding animation of a tile when the player moves it.
SLIDE_DURATION_SOLVER = 0.5 # This many seconds to finish the sliding animation of a tile when puzzle is solving itself.

BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (240, 240, 240)
TEXT_BUTTON_COLOR = (0, 0, 0)
COUNTER_FONT_COLOR = (240, 240, 240)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 640

BORDER_WIDTH = 20 # The size of the empty space between the sides of the window and the puzzle.

START_BTNS_WIDTH = 200
START_BTNS_HEIGHT = 50

PLAY_BTNS_WIDTH = 150
PLAY_BTNS_HEIGHT = START_BTNS_HEIGHT

START_MENU_BTNS_FONT_SIZE = 60
PLAY_BTNS_FONT_SIZE = 48
COUNTER_FONT_SIZE = 82

GRANDPARENT_FOLDER = Path(__file__).parent.parent
STATE_ACTION_MAP_PATH = Path(GRANDPARENT_FOLDER, 'q_tables\\state-action_map.pkl')
PUZZLE_IMG_PATH = Path(GRANDPARENT_FOLDER, 'imgs\\Shake-the-room.png') 