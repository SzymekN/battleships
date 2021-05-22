class Settings():
    def __init__(self):
        """Game settings"""
        self.screen_width = 700
        self.screen_height = 700
        self.bg_color = (230,230,230)
        self.FPS = 30 

        #tile options
        self.tile_width = 50
        self.tile_height = 50

        #board options
        self.board_margins = 100

        #ship settings
        self.max_size = 3
        self.max_trials = 20

        #score settings
        self.score_top_margin = self.tile_height*10 + self.board_margins * 1.5 

