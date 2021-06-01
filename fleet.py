class Fleet:
    """class used to initialize default ship settings in game"""

    def __init__(self, bs_game):
        self.max_size = bs_game.settings.max_size
        self.max_trials = bs_game.settings.max_trials
        self._reset_parameters()

    def _reset_parameters(self):
        """set default parameters of generating fleet"""
        self.space_available = []
        for i in range(10):
            self.space_available.append([j for j in range(10)])
        self.temp_available = self.space_available.copy()
        self.good_positions = []
        self.size = self.max_size
        self.ships_left = self.max_size + 1 - self.size
        self.trial = 0

    def check_position(self, fleet, horizontal, start_x, start_y):
        """Check if position for given size is good"""
        position_good = True
        temp_position = []
        temp_size = fleet.size+1

        while temp_size >= 0 and position_good:

            # if too many trials to generate ships, start from beginning
            if fleet.trial > fleet.max_trials:
                fleet._reset_parameters()
                position_good = False
                break

            # check if coordinates are good for horizontal alignment
            if horizontal:
                if temp_size + start_x < 0:
                    break
                elif temp_size + start_x > 9:
                    temp_size -= 1
                for i in range(-1, 2, 1):
                    if start_y+i < 0 or start_y + i > 9:
                        continue
                    if(start_x + temp_size not in fleet.space_available[start_y + i]):
                        position_good = False
                        break
                    fleet.temp_available[start_y +
                                         i].remove(start_x + temp_size)

                if temp_size != -1 and temp_size != fleet.size + 1:
                    temp_position.append(
                        (start_x+temp_size, start_y))

            # check if coordinates are good for vertical alignement
            else:
                if temp_size + start_y < 0:
                    break
                elif temp_size + start_y > 9:
                    temp_size -= 1
                for i in range(-1, 2, 1):
                    if start_x+i < 0 or start_x + i > 9:
                        continue
                    if(start_x + i not in fleet.space_available[start_y + temp_size]):
                        position_good = False
                        break
                    fleet.temp_available[start_y +
                                         temp_size].remove(start_x + i)

                if temp_size != -1 and temp_size != fleet.size + 1:
                    temp_position.append(
                        (start_x, start_y+temp_size))

            temp_size -= 1

        return position_good, temp_position

    def create_ships_dict(self, bs_game):
        """Create dictionary with ships positions and set positions as occupied"""
        ship_id = 0
        bs_game.ships = {}
        for ship in self.good_positions:
            bs_game.ships[ship_id] = ship
            ship_id += 1
            for position in ship:
                for tile in bs_game.tiles:
                    if position[1] == tile.column and position[0] == tile.row:
                        tile.occupied = True
                        break
