class GameStats:
    """Keep track on game stats"""

    def __init__(self):
        self.total_moves = 0
        self.total_games = 0
        self.end_game = False
        self.reset_stats()

    def reset_stats(self):
        """set default stats"""
        self.win = False
        self.moves = 0
        self.ships_sunk = 0
        self.sunk = {}
