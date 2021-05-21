import pygame
from pygame.sprite import Sprite

class Tile(Sprite):
    """Class represents one tile on board"""

    def __init__(self, bs_game):
        super().__init__()
        self.screen = bs_game.screen
        self.settings = bs_game.settings

        self.occupied = False
        self.sunk = False

        self.image = pygame.image.load('images/tile_default.bmp')
        self.rect = self.image.get_rect()

        self.width = self.settings.tile_width
        self.height = self.settings.tile_height

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.row = 0
        self.column = 0

    def draw_tile(self):
        """Draw tile"""
        self.screen.blit(self.image, self.rect)
