
from fleet import Fleet
import sys
import pygame
from random import choice


from settings import Settings
from tile import Tile
from label import Label


class Battleship:
    """class defines how the game works"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Battleship")

        # initialize game objects
        self.tiles = pygame.sprite.Group()
        self.labels = pygame.sprite.Group()
        self.ships = []

        # initialize game board
        self._create_board()
        self._create_ships()

    def run_game(self):
        """Start main game"""
        while True:
            pygame.time.Clock().tick(self.settings.FPS)
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond if event occurs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _create_board(self):
        """Create 10x10 board of tiles"""
        board_margin = self.settings.board_margins
        label_width = self.settings.tile_width
        label_height = self.settings.tile_height
        edge_distance = board_margin - label_height
        for label in range(10):
            pos_x = board_margin + label * label_width - 1*label
            str = chr(65+label)
            label_x = Label(self, str, pos_x, edge_distance)

            self.labels.add(label_x)

            pos_y = board_margin + label * label_height - 1*label
            str = chr(49 + label)
            if str == ":":
                str = "10"
            label_y = Label(self, str, edge_distance, pos_y)
            self.labels.add(label_y)

        for row_number in range(10):
            for column_number in range(10):
                self._create_tile(row_number, column_number)

    def _create_tile(self, row_number, column_number):
        """Create tiles in different positions"""
        tile = Tile(self)
        tile_width = tile.rect.width
        margin = self.settings.board_margins
        tile.rect.x = margin + column_number * tile_width - 1 * column_number
        tile.rect.y = margin + row_number * tile_width - 1 * row_number
        tile.row = row_number
        tile.column = column_number
        self.tiles.add(tile)

    def _create_ships(self):
        fleet = Fleet(self)

        trial_summary = 0
        reset_counter = 0
        while fleet.size >= 1:

            temp_position = []
            horizontal = False
            vertical = False
            # -1 = horizontal, 1 = vertical
            orientation = choice([-1, 1])
            if orientation == -1:
                horizontal = True
            else:
                vertical = True

            starting_y = choice(range(10 - fleet.size*vertical))
            if(len(fleet.space_available[starting_y]) == 0):
                continue

            x_trial = 0
            while x_trial < 3:
                starting_x = choice(fleet.space_available[starting_y])
                if starting_x < 10 - fleet.size*horizontal:
                    position_good = True
                    break
                else:
                    x_trial += 1
                    position_good = False

            trial_summary += x_trial
            trial_summary += 1
            temp_size = fleet.size+1
            while temp_size >= 0 and position_good:

                if fleet.trial > fleet.max_trials:
                    fleet._reset_parameters()
                    position_good = False

                    reset_counter += 1
                    trial_summary += fleet.max_trials
                    break

                if horizontal:
                    if temp_size + starting_x < 0:
                        break
                    elif temp_size + starting_x > 9:
                        temp_size -= 1
                    for i in range(-1, 2, 1):
                        if starting_y+i < 0 or starting_y + i > 9:
                            continue
                        if(starting_x + temp_size not in fleet.space_available[starting_y + i]):
                            position_good = False
                            break
                        fleet.temp_available[starting_y +
                                       i].remove(starting_x + temp_size)

                    if temp_size != -1 and temp_size != fleet.size + 1:
                        temp_position.append(
                            (starting_x+temp_size, starting_y))

                elif vertical:
                    if temp_size + starting_y < 0:
                        break
                    elif temp_size + starting_y > 9:
                        temp_size -= 1
                    for i in range(-1, 2, 1):
                        if starting_x+i < 0 or starting_x + i > 9:
                            continue
                        if(starting_x + i not in fleet.space_available[starting_y + temp_size]):
                            position_good = False
                            break
                        fleet.temp_available[starting_y +
                                       temp_size].remove(starting_x + i)

                    if temp_size != -1 and temp_size != fleet.size + 1:
                        temp_position.append(
                            (starting_x, starting_y+temp_size))

                temp_size -= 1

            if position_good:
                fleet.space_available = fleet.temp_available.copy()
                fleet.good_positions.append(temp_position)
                if(fleet.ships_left == 0):
                    fleet.size -= 1
                    fleet.ships_left = fleet.max_size + 1 - fleet.size
                else:
                    fleet.ships_left -= 1
            else:
                fleet.temp_available = fleet.space_available.copy()
                fleet.trial += 1

        print(reset_counter)
        print(trial_summary)
        draw_cost = 0
        for ship in fleet.good_positions:
            for position in ship:
                for tile in self.tiles:
                    draw_cost += 1
                    if position[0] == tile.column and position[1] == tile.row:
                        tile.image = pygame.image.load('images/tile_shot.bmp')
                        break
                    
        print(draw_cost)

    def _set_good_position(self, position_good):
        position_good = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.tiles.draw(self.screen)
        
        for label in self.labels:
            label.draw_label()

        # print(self.labels)
        pygame.display.flip()


if __name__ == '__main__':
    bs = Battleship()
    bs.run_game()
