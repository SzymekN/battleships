import pygame.font
from pygame.sprite import Sprite

class Label(Sprite):
    """class representing board labels"""

    def __init__(self, bs_game, str, pos_x, pos_y):
        super().__init__()
        self.screen = bs_game.screen
        self.settings = bs_game.settings
        self.screen_rect = self.screen.get_rect()

        self.width = self.settings.tile_width
        self.height = self.settings.tile_height
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None, 48)


        self.rect = pygame.Rect(pos_x,pos_y,self.width, self.height)
        # self.rect.midbottom = (0,0)

        self._prep_label(str)

    def _prep_label(self, str):
        """Set text to label"""
        self.label_image = self.font.render(str, True, self.text_color)
        self.label_image_rect = self.label_image.get_rect()
        self.label_image_rect.center = self.rect.center

    def draw_label(self):
        self.screen.blit(self.label_image, self.label_image_rect)
    