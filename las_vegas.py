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
        # set available tiles to shoot at
        for i in range(10):
            self.to_check.append([j for j in range(10)])
        self.known_positions = {}

        self.deterministic_y = 0

        self.reset_close_shots()

    def reset_close_shots(self):
        # positions to shot next if any position is known
        # right, left, up, down
        self.close_shot_x_r = 1
        self.close_shot_x_l = 1
        self.close_shot_y_u = 1
        self.close_shot_y_d = 1

        # next tile to check on right/left or down/up
        self.next_right = True
        self.next_down = True

        # last shot hit a ship
        self.shot_succesful = True

    def las_vegas(self):
        """Randomized algorithm to solve battleships"""
        if self.stats.win == False:
            x_index = -1
            y_index = -1

            # if any ship was hit but not sunk find neighbouring ship tiles
            if len(self.known_positions) != 0:
                x_index, y_index = self.shoot_close()

            # if neighbouring tile with whip not found
            if x_index == -1:
                y_index = randint(0, 9)
                if len(self.to_check[y_index]) == 0:
                    return
                x_index = choice(self.to_check[y_index])

            # remove tile from tiles to check
            self.to_check[y_index].remove(x_index)

            # calculate pointer position to click on tile
            correncting_value = self.settings.board_margins + self.settings.tile_width // 5
            y_pos = (x_index * 50) + correncting_value
            x_pos = (y_index * 50) + correncting_value

            # check if click hit anything
            self.bs_game._check_click((y_pos, x_pos))
            self.known_positions = self.stats.sunk
            self.check_if_sunk()

    def deterministic(self):
        """Deterministic algorithm to solve battleships"""
        if self.stats.win == False and self.deterministic_y < 10:
            x_index = -1
            y_index = -1

            # if any ship was hit but not sunk check neighbouring positions
            if len(self.known_positions) != 0:
                x_index, y_index = self.shoot_close()

            # if no neighbouring position foud, check next available
            if x_index == -1:
                while len(self.to_check[self.deterministic_y]) == 0:
                    self.deterministic_y += 1
                    if self.deterministic_y >= 10:
                        return
                y_index = self.deterministic_y
                x_index = self.to_check[y_index][0]

            # remove tile from tiles to check
            self.to_check[y_index].remove(x_index)

            # calculate pointer position to click on tile
            correncting_value = self.settings.board_margins + self.settings.tile_width // 5
            y_pos = (x_index * 50) + correncting_value
            x_pos = (y_index * 50) + correncting_value

            # check if click hit anything
            self.bs_game._check_click((y_pos, x_pos))
            self.known_positions = self.stats.sunk
            self.check_if_sunk()

    def shoot_close(self):
        """If any position is known shot neighbouring tiles"""
        key = next(iter(self.known_positions))
        pos = self.known_positions[key]
        pos_x = pos[0][1]
        pos_y = pos[0][0]
        next_shot = (-1, -1)

        # if last shot didn't hit any ship change direction of next shot
        if self.shot_succesful == False:
            self._direction_change()

        # if shot would hit out of board change direction of next shot
        self._in_board(pos_x, pos_y)

        # if available check neighbouring positions
        if len(pos) == 1:
            if pos_x < 9 and pos_x+1 in self.to_check[pos_y]:
                next_shot = (pos_x+1, pos_y)
                self.close_shot_x_r += 1
                self.next_right = True

            elif pos_y < 9 and pos_x in self.to_check[pos_y+1]:
                next_shot = (pos_x, pos_y+1)
                self.close_shot_y_d += 1
                self.next_down = True

            elif pos_x > 0 and pos_x-1 in self.to_check[pos_y]:
                next_shot = (pos_x-1, pos_y)
                self.close_shot_x_l += 1
                self.next_right = False

            elif pos_y > 0 and pos_x in self.to_check[pos_y-1]:
                next_shot = (pos_x, pos_y-1)
                self.close_shot_y_u += 1
                self.next_down = False

        # if two positions of a ship are known, check further tiles
        elif len(pos) > 1:
            if pos[0][0] == pos[1][0] and self.next_right and pos_x+self.close_shot_x_r in self.to_check[pos_y]:
                next_shot = (pos_x+self.close_shot_x_r, pos_y)
                self.close_shot_x_r += 1
            else:
                self.next_right = False

            if pos[0][0] == pos[1][0] and self.next_right == False and pos_x-self.close_shot_x_l in self.to_check[pos_y]:
                next_shot = (pos_x-self.close_shot_x_l, pos_y)
                self.close_shot_x_l += 1

            if pos[0][1] == pos[1][1] and self.next_down and pos_x in self.to_check[pos_y+self.close_shot_y_d]:
                next_shot = (pos_x, pos_y+self.close_shot_y_d)
                self.close_shot_y_d += 1
            else:
                self.next_down = False

            if pos[0][1] == pos[1][1] and self.next_down == False and pos_x in self.to_check[pos_y-self.close_shot_y_u]:
                next_shot = (pos_x, pos_y-self.close_shot_y_u)
                self.close_shot_y_u += 1

        return next_shot

    def _direction_change(self):
        """if last shot didn't hit anything change values"""
        if self.next_right == True:
            self.next_right = False
        elif self.next_right == False:
            self.next_right = True
        if self.next_down == True:
            self.next_down = False
        elif self.next_down == False:
            self.next_down = True

    def _in_board(self, pos_x, pos_y):
        """Check if shooting in the same direction will hit inside the game board"""
        if pos_x+self.close_shot_x_r >= 10:
            self.next_right = False
        if pos_x-self.close_shot_x_l < 0:
            self.next_right = True
        if pos_y+self.close_shot_y_d >= 10:
            self.next_down = False
        if pos_y-self.close_shot_y_u < 0:
            self.next_down = True

    def check_if_sunk(self):
        """Check if shooting at tile sunk a ship"""
        for k in self.known_positions.copy():
            # if all segments of a ship were hit
            if k not in self.bs_game.ships:
                self.horizontal = False
                first = self.known_positions[k][0]
                second = self.known_positions[k][1]

                # check if ship is aligned vertically
                if first[1] == second[1]:
                    self.horizontal = True

                first = (10, 10)
                last = (-1, -1)

                for pos in self.known_positions[k].copy():
                    if self.horizontal == False:
                        # Check what are the first and the last position for given alignement
                        if first[1] > pos[1]:
                            first = pos
                        if last[1] < pos[1]:
                            last = pos
                        x = pos[1]
                        y = pos[0]
                        self.delete_neighbours(x, y)
                    else:
                        # Check what are the first and the last position for given alignement
                        if first[0] > pos[0]:
                            first = pos
                        if last[0] < pos[0]:
                            last = pos
                        x = pos[1]
                        y = pos[0]
                        self.delete_neighbours(x, y)

                if self.horizontal:
                    # delete tile above whole ship
                    if first[0] > 0:
                        x = first[1]
                        y = first[0] - 1
                        self.delete_neighbours(x, y, True)

                    # delete tile below whole ship
                    if last[0] < 9:
                        x = last[1]
                        y = last[0] + 1
                        self.delete_neighbours(x, y, True)
                else:
                    # delete tile on the left of whole ship
                    if first[1] > 0:
                        x = first[1] - 1
                        y = first[0]
                        self.delete_neighbours(x, y, True)

                    # delete tile on the right of whole ship
                    if last[1] < 9:
                        x = last[1] + 1
                        y = last[0]
                        self.delete_neighbours(x, y, True)

                # delete current ship from known positions
                del self.known_positions[k]
                # reset values of close shooting function
                self.reset_close_shots()

    def delete_neighbours(self, x, y, del_this=False):

        pos1 = (-1, -1)
        pos2 = (-1, -1)
        pos3 = (-1, -1)

        # if this tile is neighbouring with ship delete this
        if del_this:
            if x in self.to_check[y]:
                self.to_check[y].remove(x)
            pos3 = (y, x)

        # delete tiles above and below ship
        if self.horizontal == False:
            if y - 1 >= 0:
                if x in self.to_check[y-1]:
                    self.to_check[y-1].remove(x)
                pos1 = (y - 1, x)

            if y + 1 <= 9:
                if x in self.to_check[y+1]:
                    self.to_check[y+1].remove(x)
                pos2 = (y + 1, x)

        # delete on the left on the right of a ship
        else:
            if x - 1 >= 0:
                if x - 1 in self.to_check[y]:
                    self.to_check[y].remove(x - 1)
                pos1 = (y, x-1)

            if(x+1 <= 9):
                if x + 1 in self.to_check[y]:
                    self.to_check[y].remove(x + 1)
                pos2 = (y, x+1)

        # change image of tiles
        for tile in self.bs_game.tiles:
            if tile.row == pos1[0] and tile.column == pos1[1] or tile.row == pos2[0] and tile.column == pos2[1] or tile.row == pos3[0] and tile.column == pos3[1]:
                tile.image = pygame.image.load(
                    'images/tile_banned.bmp')
