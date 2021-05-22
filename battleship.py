
from las_vegas import LasVegas
from scoreboard import Scoreboard
from game_stats import GameStats
from fleet import Fleet
import sys
import pygame
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
        self._create_ships()
        self.sb.prep_moves()

        self.ls = LasVegas(self)


    def run_game(self):
        """Start main game"""
        while True:
            pygame.time.Clock().tick(300)
            self.ls.las_vegas()
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond if event occurs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.stats.win == False:
                mouse_pos = pygame.mouse.get_pos()
                self._check_click(mouse_pos)

    def _check_click(self, mouse_pos):
        # print(mouse_pos)
        coordinates = (0, 0)
        for tile in self.tiles:
            if tile.rect.collidepoint(mouse_pos):
                coordinates = (tile.row, tile.column)
                if tile.occupied:
                    tile.image = pygame.image.load('images/tile_ship_hit.bmp')
                elif tile.sunk:
                    break
                else:
                    tile.image = pygame.image.load('images/tile_shot.bmp')
                self.stats.moves += 1

        to_delete = self.check_shot(coordinates)        

        if to_delete != None:
            del self.ships[to_delete]

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
                if k not in self.stats.sunk:
                    self.stats.sunk[k] = []
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
                    self.stats.ships_sunk +=1
                    self.sb.prep_sunk()
                    return k
                    
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
        """Generate ships positions"""
        fleet = Fleet(self)
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
                if(fleet.ships_left == 0):
                    fleet.size -= 1
                    fleet.ships_left = fleet.max_size + 1 - fleet.size
                else:
                    fleet.ships_left -= 1
            else:
                fleet.temp_available = fleet.space_available.copy()
                fleet.trial += 1

        self.ships = {}
        ship_id = 0

        # temporary function to check if generation was acceptable - to be deleted
        for ship in fleet.good_positions:
            self.ships[ship_id] = ship
            ship_id += 1
            for position in ship:
                for tile in self.tiles:
                    if position[1] == tile.column and position[0] == tile.row:
                        tile.occupied = True
                        # tile.image = pygame.image.load('images/tile_shot.bmp')
                        break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.tiles.draw(self.screen)

        for label in self.labels:
            label.draw_label()

        self.sb.show_score()

        if self.stats.win:
            self.sb.show_win()
        
        # print(self.labels)
        pygame.display.flip()


if __name__ == '__main__':
    bs = Battleship()
    bs.run_game()
