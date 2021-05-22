from random import randint, choice
from pprint import pprint
import pygame.time


class LasVegas:
    """Randomized algorithm for battleships game"""

    def __init__(self, bs_game):
        self.bs_game = bs_game
        self.stats = bs_game.stats
        self.settings = bs_game.settings

        self.reset_values()

    def reset_values(self):
        self.to_check = []
        for i in range(10):
            self.to_check.append([j for j in range(10)])
        self.known_positions = {}

        self.deterministic_y = 0

    def las_vegas(self):
        if self.stats.win == False:
            y_index = randint(0, 9)
            if len(self.to_check[y_index]) == 0:
                return
            x_index = choice(self.to_check[y_index])
            self.to_check[y_index].remove(x_index)
            correncting_value = self.settings.board_margins + self.settings.tile_width // 5
            y_pos = (x_index * 50) + correncting_value
            x_pos = (y_index * 50) + correncting_value

            if y_pos < 100 or y_pos > 590:
                print(y_pos)
            self.bs_game._check_click((y_pos, x_pos))
            self.known_positions = self.stats.sunk
            self.check_if_sunk()
    
    def deterministic(self):
        if self.stats.win == False and self.deterministic_y < 10:
            while len(self.to_check[self.deterministic_y]) == 0:
                self.deterministic_y += 1
                if self.deterministic_y >= 10:
                    return

            y_index = self.deterministic_y
            x_index = self.to_check[y_index][0]
            self.to_check[y_index].remove(x_index)
            correncting_value = self.settings.board_margins + self.settings.tile_width // 5
            y_pos = (x_index * 50) + correncting_value
            x_pos = (y_index * 50) + correncting_value

            if y_pos < 100 or y_pos > 590:
                print(y_pos)
            self.bs_game._check_click((y_pos, x_pos))
            self.known_positions = self.stats.sunk
            self.check_if_sunk()
    

    def check_if_sunk(self):
            for k in self.known_positions.copy():
                if k not in self.bs_game.ships:
                    self.vertical = False
                    first = self.known_positions[k][0]
                    second = self.known_positions[k][1]
                    if first[1] == second[1]:
                        self.vertical = True
                    
                    first = (10, 10)
                    last = (-1, -1)
                    for pos in self.known_positions[k].copy():
                        if self.vertical:
                            # check if coordinates are good for self.vertical alignement
                            if first[0] > pos[0]:
                                first = pos
                            if last[0] < pos[0]:
                                last = pos
                            x = pos[1]
                            y = pos[0]
                            self.delete_neighbours(x, y)
                        else:
                            # check if coordinates are good for self.vertical alignement
                            if first[1] > pos[1]:
                                first = pos
                            if last[1] < pos[1]:
                                last = pos
                            x = pos[1]
                            y = pos[0]
                            self.delete_neighbours(x, y)

                    if self.vertical:
                        if first[0] > 0:
                            x = first[1]
                            y = first[0] - 1
                            self.delete_neighbours(x, y, True)

                        if last[0] < 9:
                            x = last[1]
                            y = last[0] + 1
                            self.delete_neighbours(x, y, True)
                    else:
                        if first[1] > 0:
                            x = first[1] - 1
                            y = first[0]
                            self.delete_neighbours(x, y, True)

                        if last[1] < 9:
                            x = last[1] + 1
                            y = last[0] 
                            self.delete_neighbours(x, y, True)

                    del self.known_positions[k]

    def delete_neighbours(self, x, y, del_this=False):

        pos1 = (-1, -1)
        pos2 = (-1, -1)
        pos3 = (-1, -1)
        if del_this:
            if x in self.to_check[y]:
                self.to_check[y].remove(x)
            pos3 = (y, x)

        if self.vertical:
            if x - 1 >= 0:
                if x - 1 in self.to_check[y]:
                    self.to_check[y].remove(x - 1)
                pos1 = (y, x-1)

            if(x+1 <= 9):
                if x + 1 in self.to_check[y]:
                    self.to_check[y].remove(x + 1)
                pos2 = (y, x+1)
        else:
            if y - 1 >= 0:
                if x in self.to_check[y-1]:
                    self.to_check[y-1].remove(x)
                pos1 = (y -1, x)

            if y +1 <= 9:
                if x in self.to_check[y+1]:
                    self.to_check[y+1].remove(x)
                pos2 = (y +1 , x)

        for tile in self.bs_game.tiles:
            if tile.row == pos1[0] and tile.column == pos1[1] or tile.row == pos2[0] and tile.column == pos2[1] or tile.row == pos3[0] and tile.column == pos3[1]:
                tile.image = pygame.image.load(
                    'images/tile_banned.bmp')
