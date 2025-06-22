import math
import pygame

import game_constants as gc

class Button:
    def __init__(self, screen, width, height, text, font, center=None, bottom_left=None, bottom_right=None):
        self.screen = screen
        self.btn = pygame.Rect((0, 0), (width, height))
        self.text = text
        self.font = font

        if center is not None:
            self.btn.center = center
        elif bottom_left is not None:
            self.btn.bottomleft = bottom_left
        elif bottom_right is not None:
            self.btn.bottomright = bottom_right
        else:
            raise ValueError("At least on of the arguments 'center' or 'lower_left' must not be None.")

    @staticmethod
    def _distance(p1, p2):
        x = p1[0] - p2[0]
        y = p1[1] - p2[1]
        return math.sqrt(x * x + y * y)
    
    def draw(self):
        pygame.draw.rect(self.screen, rect=self.btn, color=gc.BUTTON_COLOR, border_radius=max(self.btn.width, self.btn.height))

        t = self.font.render(self.text, True, gc.TEXT_BUTTON_COLOR)
        self.screen.blit(t, t.get_rect(center=self.btn.center))

    def erase(self, color):
        """Fills the button with the given color."""
        pygame.draw.rect(self.screen, rect=self.btn, color=color, border_radius=max(self.btn.width, self.btn.height))

    def check_btn_press(self, point):
        """
        Returns true if the point is inside the button.
        """
        
        """
        Buttons have rounded sides (semicircles) so we make additional checks to exclude the "corners".

                       |--------------------------------------------|
                  |--- :                                            : ---|
             |---      :                                            :      ---|
           |-          :                                            :          -|
          |            :                                            :            |
          |      2     O                     1                      O      3     |
          |            :                                            :            |
           |-          :                                            :          -|
             |---      :                                            :      ---|
                  |--- :                                            : ---|
                       |--------------------------------------------|

        We check if the point is in rectangle 1 or in the two circles 2 and 3.
        The two 'O' represent the centers of the (semi)circles. They are the 'midleft' and 'midright' points of rectangle 1.
        """
        r = pygame.Rect((0, 0), (self.btn.width - self.btn.height, self.btn.height)) # Rectangle 1
        r.center = self.btn.center

        return r.collidepoint(point) or \
            Button._distance(r.midleft, point) <= r.height / 2 or \
            Button._distance(r.midright, point) <= r.height / 2