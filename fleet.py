class Fleet:
    """class used to initialize default ship settings in game"""

    def __init__(self, bs_game):
        self.max_size = bs_game.settings.max_size
        self.max_trials = bs_game.settings.max_trials
        self._reset_parameters()

    def _reset_parameters(self):
        self.space_available = []
        for i in range(10):
            self.space_available.append([j for j in range(10)])
        self.temp_available = self.space_available.copy()
        self.good_positions = []
        self.size = self.max_size
        self.ships_left = self.max_size + 1 - self.size
        self.trial = 0
