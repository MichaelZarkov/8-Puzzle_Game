import math
import pygame
import sys

from button import Button
from counter import Counter
import game_constants as gc
from sliding_puzzle import SlidingPuzzleGame
from solver import Solver
from start_menu import StartMenu

class Game:

    def __init__(self):
        self.puzzle = SlidingPuzzleGame() # Contains the puzzle logic.
        self.solver = Solver(gc.STATE_ACTION_MAP_PATH)
        self.tile_size, self.tiles = self._load_puzzle_pieces()

        pygame.init()  
        pygame.display.set_caption('8-puzzle')
        self.screen = pygame.display.set_mode(size=(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        self.move_counter = Counter(self.screen, (gc.SCREEN_WIDTH // 2, gc.BORDER_WIDTH * 4 + self.tile_size * 3))

        self._start_game()

        pygame.quit()

    @staticmethod
    def _load_puzzle_pieces():
        """
        Reads an image, resizes it so that it fits in the width of the screen, slices it, and returns
        the 9 puzzle pieces with aditional info to operate with them.
        Returns the side length of the pieces.
        Requires the input image to be square.
        """

        img = pygame.image.load(gc.PUZZLE_IMG_PATH)
        assert img.get_width() == img.get_height(), "Puzzle image must be square."

        img_size = gc.SCREEN_WIDTH - gc.BORDER_WIDTH * 2
        resized_img = pygame.transform.smoothscale(img, (img_size, img_size))

        tile_size = img_size // 3

        # Slice the image.
        tiles = []
        for row in range(0, 3):
            for col in range(0, 3):
                rect = pygame.Rect((col * tile_size, row * tile_size), (tile_size, tile_size))
                tiles.append({
                    'number': row * 3 + col + 1, 
                    'tile': resized_img.subsurface(rect),
                    'rect': rect # Give the tile a corresponding rectangle. 
                })

        tiles[8]['number'] = 0 # Bottom right tile is the empty spot.

        return tile_size, tiles

    def _position_puzzle_pieces(self):
        """
        Positions the puzzle pieces in a grid in the order they appear in 'self.tiles'.
        """

        # In Pygame it is easiest to associate an image (surface) with a rectangle and let the rectangle handle the moving logic.
        # When we display a tile on the screen we will be using the position of its corresponding rectangle.
        for i in range(0, 9):
            row = i // 3
            col = i % 3

            x = gc.BORDER_WIDTH + col * self.tile_size # Horizontal offset from top left corner.
            y = gc.BORDER_WIDTH + row * self.tile_size # Vertical offset form top left corner.

            self.tiles[i]['rect'].topleft = (x, y)

    def _create_playscreen_buttons(self):
        font = pygame.font.Font(None, gc.PLAY_BTNS_FONT_SIZE)

        back = Button(
            screen=self.screen,
            width=gc.PLAY_BTNS_WIDTH,
            height=gc.PLAY_BTNS_HEIGHT,
            text='Back',
            font=font,
            bottom_left=(gc.BORDER_WIDTH, gc.SCREEN_HEIGHT - gc.BORDER_WIDTH)
        )

        shuffle = Button(
            screen=self.screen,
            width=gc.PLAY_BTNS_WIDTH,
            height=gc.PLAY_BTNS_HEIGHT,
            text='Shuffle',
            font=pygame.font.Font(None, gc.PLAY_BTNS_FONT_SIZE),
            bottom_right=(gc.SCREEN_WIDTH - gc.BORDER_WIDTH, gc.SCREEN_HEIGHT - gc.BORDER_WIDTH)
        )

        solve = Button(
            screen=self.screen,
            width=gc.PLAY_BTNS_WIDTH,
            height=gc.PLAY_BTNS_HEIGHT,
            text='Solve',
            font=pygame.font.Font(None, gc.PLAY_BTNS_FONT_SIZE),
            bottom_right=(gc.SCREEN_WIDTH - gc.BORDER_WIDTH, gc.SCREEN_HEIGHT - gc.BORDER_WIDTH)
        )

        return back, shuffle, solve

    def _draw_tiles(self):
        """
        Draw the tiles one by one.
        """
        clock = pygame.time.Clock()
        for tile in filter(lambda x: x['number'] != 0, self.tiles):
            self.screen.blit(tile['tile'], tile['rect'])
            pygame.display.flip()

            clock.tick(gc.TILE_DRAW_DELAY)

    def _shuffle(self):
        self.puzzle.shuffle()

        new_tile_arrangement = []
        for num in self.puzzle.board:
            for tile in self.tiles:
                if tile['number'] == num:
                    new_tile_arrangement.append(tile)
                    break
        
        self.tiles = new_tile_arrangement
        self._position_puzzle_pieces()

    def _animate_tile_slide(self, tile_index, hole_index, slide_duration_seconds):
        """
        Animates the sliding of the tile to the empty spot.
        Expects valid input.
        'tile_index' - index of the tile in the list before the slide.
        'hole_index' - index of the hole in the list before the slide.
        """
        """
        Note: The way we animate the sliding of tiles is alright for this game but I think it can be done better. At the moment the
        '_play()' function has its own "game loop" which doesn't handle events (player input). This is not very nice because the
        game may seem unresponsive when given commands during the animation.
        """

        # Find direction of the slide.
        if hole_index == tile_index - 3:
            direction = 'u'
        elif hole_index == tile_index + 1:
            direction = 'r'
        elif hole_index == tile_index + 3:
            direction = 'd'
        elif hole_index == tile_index - 1:
            direction = 'l'

        # Save this for the final shift.
        tile_center_before_shift = self.tiles[tile_index]['rect'].center
        tile_center_after_shift = self.tiles[hole_index]['rect'].center

        self.tiles[hole_index]['rect'].center = tile_center_before_shift # Hole is invisible so move it right away.

        frames = math.ceil(gc.FPS * slide_duration_seconds) # Number of animation frames.
        dx = self.tile_size / frames # Distance moved per frame.

        rect = self.tiles[tile_index]['rect']
        tile = self.tiles[tile_index]['tile']

        # Animate slide.
        clock = pygame.time.Clock()
        offset = 0
        for _ in range(frames - 1):
            pygame.draw.rect(self.screen, rect=rect, color=gc.BACKGROUND_COLOR) # Erase the tile.

            # Move the rectangle.
            offset += dx
            if direction == 'u':
                rect.center = (tile_center_before_shift[0], tile_center_before_shift[1] - offset)
            elif direction == 'r':
                rect.center = (tile_center_before_shift[0] + offset, tile_center_before_shift[1])
            elif direction == 'd':
                rect.center = (tile_center_before_shift[0], tile_center_before_shift[1] + offset)
            elif direction == 'l':
                rect.center = (tile_center_before_shift[0] - offset, tile_center_before_shift[1])
            
            self.screen.blit(tile, rect)
            pygame.display.flip()

            clock.tick(gc.FPS)

        # Set the final position exactly.
        pygame.draw.rect(self.screen, rect=rect, color=gc.BACKGROUND_COLOR)
        rect.center = tile_center_after_shift
        self.screen.blit(tile, rect)
        pygame.display.flip()

        # Swap tile and hole positions in the list.
        self.tiles[tile_index], self.tiles[hole_index] = self.tiles[hole_index], self.tiles[tile_index]

    def _is_point_on_tile(self, point):
        """
        If the point is on a tile, returns its index in the list.
        Returns None otherwise (including when the point is on the hole).
        """

        for i in range(0,9):
            if self.tiles[i]['rect'].collidepoint(point) and self.tiles[i]['number'] != 0:
                return i
        
        return None

    def _solve(self, solve, back):
        solve.erase(gc.BACKGROUND_COLOR)
        back.erase(gc.BACKGROUND_COLOR)

        while not self.puzzle.is_solved():
            tile_index, hole_index = self.puzzle.move_hole(self.solver.get_action(self.puzzle))
            self.move_counter.increment() 
            self._animate_tile_slide(tile_index, hole_index, gc.SLIDE_DURATION_SOLVER)

            # Allow the closing of the window during the solving process.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def _move_tile(self, tile_index):
        """
        Moves the tile to the adjacent empty spot.
        Increments the move_counter.
        Does nothing if none of the four adjacent spots are empty.
        """
        hole_index = self.puzzle.move_tile_by_index(tile_index)
        if hole_index is not None:
            self.move_counter.increment()
            self._animate_tile_slide(tile_index, hole_index, gc.SLIDE_DURATION_PLAYER)

    def _draw_shuffled_screen(self, back_btn, solve_btn):
        """Draws the screen after a new tile shuffle."""
        self._shuffle()
        self.screen.fill(gc.BACKGROUND_COLOR)
        back_btn.draw()
        self._draw_tiles()
        self.move_counter.zero()
        solve_btn.draw()
        pygame.display.flip()

    def _draw_solved_screen(self, shuffle_btn):
        self.screen.blit(self.tiles[8]['tile'], self.tiles[8]['rect']) # Draw the invisible tile (hole) when solved.
        shuffle_btn.draw()
        pygame.display.flip()

    def _play(self):
        """
        The play window.
        """

        back, shuffle, solve = self._create_playscreen_buttons()

        self._draw_shuffled_screen(back, solve)

        # Keep track of mousedown events (a button is considered pressed on click and release).
        is_tile_pressed = [False for _ in range(9)]
        is_back_pressed = False
        is_solve_pressed = False
        is_shuffle_pressed = False
        is_solved = False

        pygame.event.clear() # Acceps player input after done drawing.
        clock = pygame.time.Clock()
        while True:
            clock.tick(gc.FPS)

            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tile_index = self._is_point_on_tile(event.pos)
                    if not is_solved and tile_index is not None:
                        is_tile_pressed[tile_index] = True
                    elif back.check_btn_press(event.pos):
                        is_back_pressed = True
                    elif not is_solved and solve.check_btn_press(event.pos):
                        is_solve_pressed = True
                    elif is_solved and shuffle.check_btn_press(event.pos):
                        is_shuffle_pressed = True

                elif event.type == pygame.MOUSEBUTTONUP:

                    tile_index = self._is_point_on_tile(event.pos)
                    if tile_index is not None and is_tile_pressed[tile_index]:
                        self._move_tile(tile_index)
                        if self.puzzle.is_solved():
                            self._draw_solved_screen(shuffle)
                            is_solved = True
                            
                    elif back.check_btn_press(event.pos) and is_back_pressed:
                        return
                    
                    elif not is_solved and solve.check_btn_press(event.pos) and is_solve_pressed:
                        self._solve(solve, back)
                        back.draw()
                        self._draw_solved_screen(shuffle)
                        is_solved = True
                        pygame.event.clear() # Acceps player input after done drawing.

                    elif is_solved and shuffle.check_btn_press(event.pos) and is_shuffle_pressed:
                        self._draw_shuffled_screen(back, solve)
                        is_solved = False
                        pygame.event.clear() # Acceps player input after done drawing.

                    # Reset mousedown trackers.
                    for i in range(0,9): is_tile_pressed[i] = False
                    is_back_pressed = False
                    is_solve_pressed = False
                    is_shuffle_pressed = False

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def _start_game(self):
        start_menu = StartMenu(self.screen)
        
        while True:
            command = start_menu.draw()

            if command == 'play':
                self._play()
            elif command == 'quit':
                return