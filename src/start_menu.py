import pygame

from button import Button
import game_constants as gc

class StartMenu:

    def __init__(self, screen):
        self.screen = screen

    def _draw_start_buttons(self):
        """
        Returns the rectangles of the buttons.
        """

        font = pygame.font.Font(None, gc.START_MENU_BTNS_FONT_SIZE)
        btn_spacing = 44

        play_btn = Button(
            screen=self.screen,
            width=gc.START_BTNS_WIDTH,
            height=gc.START_BTNS_HEIGHT,
            text='Play',
            font=font,
            center=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 - btn_spacing)
        )

        quit_btn = Button(
            screen=self.screen,
            width=gc.START_BTNS_WIDTH,
            height=gc.START_BTNS_HEIGHT,
            text='Quit',
            font=font,
            center=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + btn_spacing)
        )

        play_btn.draw()
        quit_btn.draw()

        return play_btn, quit_btn   

    def draw(self):
        """
        GUI of the start menu. Returns a 'play' or 'quit' command.
        """

        # Draw and display the start menu.
        self.screen.fill(gc.BACKGROUND_COLOR)
        play_btn, quit_btn = self._draw_start_buttons()
        pygame.display.flip()

        # Get input from user (wait for them to click on a button).
        mouse_down_inside_button = { 'play': False, 'quit': False } # Keep track of click and release inside the button.
        clock = pygame.time.Clock()

        while True:
            clock.tick(gc.FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_btn.check_btn_press(event.pos):
                        mouse_down_inside_button['play'] = True
                    elif quit_btn.check_btn_press(event.pos):
                        mouse_down_inside_button['quit'] = True

                elif event.type == pygame.MOUSEBUTTONUP:                
                    if mouse_down_inside_button['play'] and play_btn.check_btn_press(event.pos):
                        return 'play'
                    if mouse_down_inside_button['quit'] and quit_btn.check_btn_press(event.pos):
                        return 'quit'

                    # Reset the release tracker.
                    mouse_down_inside_button['play'] = False
                    mouse_down_inside_button['quit'] = False

                elif event.type == pygame.QUIT:
                    return 'quit'