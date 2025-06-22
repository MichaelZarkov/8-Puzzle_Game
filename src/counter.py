import pygame

import game_constants as gc

class Counter:

    def __init__(self, screen, center):
        self.screen = screen
        self.center = center # (x, y)
        self.font = pygame.font.Font(None, gc.COUNTER_FONT_SIZE)
        self.n = 0

    def erase(self):
        text = self.font.render(str(self.n), True, gc.COUNTER_FONT_COLOR)
        rect = text.get_rect(center=self.center)

        pygame.draw.rect(self.screen, rect=rect, color=gc.BACKGROUND_COLOR)

    def draw(self):
        text = self.font.render(str(self.n), True, gc.COUNTER_FONT_COLOR)
        rect = text.get_rect(center=self.center)
        self.screen.blit(text, rect)

    def increment(self):
        """
        Increments the counter.
        Draws the number on the screen.
        """
        self.erase()
        self.n += 1
        self.draw()
        
    def zero(self):
        """
        Zero out the counter.
        Draw 0 on screen
        """
        self.erase()
        self.n = 0
        self.draw()