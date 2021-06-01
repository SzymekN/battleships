import pygame.font
import pygame.surface


class Scoreboard:
    """Graphic score representation"""

    def __init__(self, bs_game) -> None:
        """initialize default scoreboard settings"""
        self.bs_game = bs_game
        self.stats = bs_game.stats
        self.settings = bs_game.settings
        self.screen = bs_game.screen

        # default settings
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        self.top_margin = self.settings.score_top_margin

        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 36)

        # prepare move counter
        self.prep_moves()
        # prepare ships sunk counter
        self.prep_sunk()
        # prepare win screen
        self.prep_win()

    def prep_moves(self):
        """Prepare move counter"""
        moves = self.stats.moves
        moves_str = f'Moves: {moves}'

        self.moves_image = self.font.render(moves_str, True, self.text_color)
        self.moves_rect = self.moves_image.get_rect()
        self.moves_rect.left = self.settings.board_margins * 1.5
        self.moves_rect.bottom = self.top_margin

    def prep_sunk(self):
        """Prepare sunk ships sounter"""
        sunk = self.stats.ships_sunk
        sunk_str = f'Sunk: {sunk}'

        self.sunk_image = self.font.render(sunk_str, True, self.text_color)
        self.sunk_rect = self.sunk_image.get_rect()
        self.sunk_rect.left = self.settings.board_margins * 4
        self.sunk_rect.bottom = self.top_margin

    def prep_win(self):
        """Prepare win screen"""
        self.screen_rect = self.screen.get_rect()
        self.background = pygame.Surface(
            (self.screen_width, self.screen_height))
        self.background.set_alpha(200)
        self.background.fill((255, 255, 255))

        win_font = pygame.font.SysFont(None, 60)
        self.win_image = win_font.render("WIN!!!", True, self.text_color)
        self.win_rect = self.win_image.get_rect()
        self.win_rect.center = self.screen_rect.center

    def show_score(self):
        """Show move and ships sunk counters"""
        self.screen.blit(self.moves_image, self.moves_rect)
        self.screen.blit(self.sunk_image, self.sunk_rect)

    def show_win(self):
        """Show win screen"""
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.win_image, self.win_rect)
        self.screen.blit(self.moves_image, self.moves_rect)
        self.screen.blit(self.sunk_image, self.sunk_rect)
