import pygame.font

class Scoreboard:
    """Graphic score representation"""

    def __init__(self, bs_game) -> None:
        self.bs_game = bs_game
        self.stats = bs_game.stats
        self.settings = bs_game.settings
        self.screen = bs_game.screen

        self.top_margin = self.settings.score_top_margin

        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None, 36)

        self.prep_moves()
        self.prep_sunk()


    def prep_moves(self):
        moves = self.stats.moves
        moves_str = f'Moves: {moves}'

        self.moves_image = self.font.render(moves_str, True, self.text_color)
        self.moves_rect = self.moves_image.get_rect()
        self.moves_rect.left = self.settings.board_margins * 1.5
        self.moves_rect.bottom = self.top_margin


    def prep_sunk(self):
        sunk = self.stats.ships_sunk
        sunk_str = f'Sunk: {sunk}'

        self.sunk_image = self.font.render(sunk_str, True, self.text_color)
        self.sunk_rect = self.sunk_image.get_rect()
        self.sunk_rect.left = self.settings.board_margins * 4
        self.sunk_rect.bottom = self.top_margin

    def show_score(self):
        self.screen.blit(self.moves_image, self.moves_rect)
        self.screen.blit(self.sunk_image, self.sunk_rect)