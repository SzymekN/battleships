import sys
import pygame
import time as t
from pygame import time
from fleet import Fleet
from random import choice


from settings import Settings
from tile import Tile
from label import Label
from game_stats import GameStats
from scoreboard import Scoreboard
from las_vegas import LasVegas


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
        self.stats = GameStats()
        self.sb = Scoreboard(self)

        # initialize game board
        self._create_board()
        self._create_tiles()
        self._create_ships()
        self.sb.prep_moves()

        self.ls = LasVegas(self)

    def run_game(self):
        """Start main game"""
        self.start = t.time()
        while True:
            # a = input("w")
            pygame.time.Clock().tick(30)
            if self.settings.deterministic:
                self.ls.deterministic()
            elif self.settings.las_vegas:
                self.ls.las_vegas()
            self._check_events()
            self._update_screen()

            if self.stats.win and self.stats.end_game == False:
                self.reset_game()

    def reset_game(self):
        """Reset whole game"""

        # set default tile values
        for tile in self.tiles:
            tile.occupied = False
            tile.sunk = False
            tile.image = pygame.image.load('images/tile_default.bmp')

        # update stats
        self.stats.total_games += 1
        self.stats.total_moves += self.stats.moves

        print(self.stats.total_games)
        # if max number of games reached stop game
        if self.stats.total_games == self.settings.max_games:
            self.end = t.time()
            print(f'Total moves: {self.stats.total_moves}')
            print(
                f'AVG moves: {self.stats.total_moves / self.stats.total_games}')
            print(f'Time elapsed: {self.end - self.start}')
            self.stats.end_game = True

        self._create_ships()
        self.ls.reset_values()
        self.stats.reset_stats()

    def _check_events(self):
        """Respond if event occurs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.stats.win == False:
                mouse_pos = pygame.mouse.get_pos()
                self._check_click(mouse_pos)

    def _check_click(self, mouse_pos):
        """Check if clicked on any tile"""
        coordinates = (0, 0)
        for tile in self.tiles:
            if tile.rect.collidepoint(mouse_pos):

                # update move count stat
                self.stats.moves += 1
                # get indexes of tile that collided with pointer
                coordinates = (tile.row, tile.column)

                # if there is a ship on current tile change image
                if tile.occupied:
                    tile.image = pygame.image.load('images/tile_ship_hit.bmp')
                    self.ls.shot_succesful = True
                    break
                # if already whole ship sunk
                elif tile.sunk:
                    break
                else:
                    tile.image = pygame.image.load('images/tile_shot.bmp')
                    self.ls.shot_succesful = False
                    break

        # check if whole ship got sunk
        to_delete = self.check_shot(coordinates)

        # if whole ship sunk remove from alive ships
        if to_delete != None:
            del self.ships[to_delete]

        # if last ship sunk, game is won
        if not self.ships:
            self.stats.win = True
            print("WIN")

        self.sb.prep_moves()

    def check_shot(self, coordinates):
        """Functions checks if shot hit any ship"""

        for k in self.ships:
            if coordinates in self.ships[k]:

                # remove coordianates from list containing ships alive
                index = self.ships[k].index(coordinates)
                value = self.ships[k].pop(index)

                # if this ship wasn't hit yet
                if k not in self.stats.sunk:
                    self.stats.sunk[k] = []

                # add position of a segment of this ship
                self.stats.sunk[k].append(value)

                # if all segments of a ship were shot, change image and delete key
                if len(self.ships[k]) == 0:
                    for pos in self.stats.sunk[k]:
                        for tile in self.tiles:
                            if tile.row == pos[0] and tile.column == pos[1]:
                                tile.image = pygame.image.load(
                                    'images/tile_ship_sunk.bmp')
                                tile.sunk = True
                                tile.occupied = False

                    # update sunk ships counter and make new label
                    self.stats.ships_sunk += 1
                    self.sb.prep_sunk()
                    return k

    def _create_board(self):
        """Create 10x10 board of tiles"""

        board_margin = self.settings.board_margins
        label_width = self.settings.tile_width
        label_height = self.settings.tile_height
        edge_distance = board_margin - label_height

        # create board labels
        for label in range(10):
            pos_x = board_margin + label * label_width - 1 * label
            str = chr(65+label)
            label_x = Label(self, str, pos_x, edge_distance)

            self.labels.add(label_x)

            pos_y = board_margin + label * label_height - 1 * label
            str = chr(49 + label)
            if str == ":":
                str = "10"
            label_y = Label(self, str, edge_distance, pos_y)

            self.labels.add(label_y)

    def _create_tiles(self):
        """Create tiles in different positions"""
        margin = self.settings.board_margins

        # initialize tiles and give them default positions
        for row_number in range(10):
            for column_number in range(10):
                tile = Tile(self)
                tile_width = tile.rect.width
                tile.rect.x = margin + column_number * tile_width - 1 * column_number
                tile.rect.y = margin + row_number * tile_width - 1 * row_number
                tile.row = row_number
                tile.column = column_number
                self.tiles.add(tile)

    def _create_ships(self):
        """Generate ships positions"""

        fleet = Fleet(self)

        # look for positions until all ships are created = until size of a ship to create > 0
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

            # choose y coordinate of ship
            starting_y = choice(range(10 - fleet.size*vertical))
            if(len(fleet.space_available[starting_y]) == 0):
                continue

            # try to choose x coordinate of a ship if space is available
            x_trial = 0
            while x_trial < 3:
                starting_x = choice(fleet.space_available[starting_y])
                if starting_x < 10 - fleet.size*horizontal:
                    position_good = True
                    break
                else:
                    x_trial += 1
                    position_good = False

            # check if choosen starting coordinates are good for given size
            position_good, temp_position = fleet.check_position(
                fleet, horizontal, starting_x, starting_y)

            # if position is good save coordinates
            if position_good:
                fleet.space_available = fleet.temp_available.copy()
                fleet.good_positions.append(temp_position)

                # if no ships left, decrease next ship size and set new value to ships_left
                if fleet.ships_left == 0:
                    fleet.size -= 1
                    fleet.ships_left = fleet.max_size + 1 - fleet.size
                else:
                    fleet.ships_left -= 1
            else:
                fleet.temp_available = fleet.space_available.copy()
                fleet.trial += 1

        # save ships positions
        fleet.create_ships_dict(self)

    def _update_screen(self):
        """Update objects on screen"""
        self.screen.fill(self.settings.bg_color)
        self.tiles.draw(self.screen)

        for label in self.labels:
            label.draw_label()

        self.sb.show_score()

        pygame.display.flip()


if __name__ == '__main__':
    bs = Battleship()
    bs.run_game()
