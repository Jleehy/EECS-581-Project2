# 9/23/2024

# Easy (0) - fully random
# Medium (1)
    # self.hit[] - array of hits / current hit
    # self.near[] - array of surrounding valid coordinates of a hit

    # If self.near is empty:
    # Get random coordinate
    # If it is a hit, append to self.hits[]
        # Populate self.near[] with all of the valid surrounding coordinates
    # In any other case, the first choice should be a coordinate from self.near[]
    # After that coordinate is used, it should be removed from the array

# Hard (2) - has access to all enemy ship coordinates
    # Array with all enemy coordinate pairs that is popped each turn

"""
Ai Class
    def __init__
        self.difficulty: int representing difficulty level
        self.ships: list of Ships
        self.num_alive_ships: int representing the number of active ships
        self.attacks: list of previous attack coordinates

        if difficulty == 1:
            self.near: list of coordinates orthogonal to the most recent successful attack
        elif difficulty == 2:
            self.enemy_coordinates: list of enemy ship coordinates

    def _get_random_coord():
        While True:
            coord = random
            if coord not in self.attacks:
                return coord

    def attack()
        coord = _get_random_coord()
        match self.difficulty
            case 0
                self.attacks.append(coord)
                return coord
            case 1
                if len(self.near) > 0
                    coord = self.near[0]
                    self.near = self.near[1:]

                self.attacks.append(coord)
                return coord
            case 2
                coord = self.enemy_coordinates[0]
                self.enemy_coordinates = self.enemy_coordinates[1:]
                return coord

    def update_after_attack(coord, result)
        if difficulty == 2
            if not self.near and result == hit
                _get_surrounding_coordinates(coord)
            else if result == sink
                self.near = []
"""

"""
Ai Class
    def __init__
        self.difficulty: int representing difficulty level
        self.ships: list of Ships
        self.num_alive_ships: int representing the number of active ships
        self.attacks: list of previous attack coordinates

        if difficulty == 1:
            self.near: list of coordinates orthogonal to the most recent successful attack
        elif difficulty == 2:
            self.enemy_coordinates: list of enemy ship coordinates

    def _get_random_coord():
        While True:
            coord = random
            if coord not in self.attacks:
                return coord

    def attack()
        coord = _get_random_coord()
        match self.difficulty
            case 0
                self.attacks.append(coord)
                return coord
            case 1
                if len(self.near) > 0
                    coord = self.near[0]
                    self.near = self.near[1:]

                self.attacks.append(coord)
                return coord
            case 2
                coord = self.enemy_coordinates[0]
                self.enemy_coordinates = self.enemy_coordinates[1:]
                return coord

    def update_after_attack(coord, result)
        if difficulty == 2
            if not self.near and result == hit
                _get_surrounding_coordinates(coord)
            else if result == sink
                self.near = []
"""

import random
import string
from player import Player
from ship import Ship
from exceptions import AlreadyFiredError

class Ai(Player):
    def __init__(self, difficulty, opponent, ships: list[Ship] = None) -> None:
        self.difficulty = difficulty #difficulty of the ai
        self.enemy_coordinates = [] #coordinates of the oposing players ships
        self._name = "AI"

        # For medium difficulty, the AI needs to track the most recent hit, and the surrounding coordinates of the hit
        # self.near is an array of the surrounding coordinates and will be used for moves after there is a hit
        if(difficulty == 1):
            self.hits = []
            self.near = []
        elif(difficulty == 2):
            #for each coordinate in each ship in the opponent's list of ships, we add the coordinate to self._enemy_coordinates
            for ship in opponent.ships:
                for coor in ship.hull:
                    temp = coor[:2]
                    self.enemy_coordinates.append(temp)
        
        # If ships is None, set self._ships to an empty list            
        if ships is None:
            self._ships = []
        else:
            self._ships: list[Ship] = ships

        #hold the state of the board. the i,j entry of the board represents the if a shot has been fired at coordinate i,j.
        #note that this contains NO information about whether that was a hit or a miss, that information is tracked by each ship.
        self._board_state: list[list[bool]] = [ [ False for _ in range(10) ] for _ in range(10) ]

        self._num_alive_ships: int = len(self._ships)

    # Returns a string literal of a randomly generated coordinate
    def get_random_coordinate(self):
        col = random.choice(string.ascii_uppercase[:10])
        row = str(random.randint(1,10))
        
        return col+row

    # Populates self.near[] after a ship is hit with valid surrounding coordinates, excluding diagonals
    def get_surrounding_coordinates(self, coordinate):

        # Parse and cast coordinate string to extract column and row
        col = coordinate[0]
        row = int(coordinate[1:])

        # Define valid columns (A-J)
        valid_cols = "ABCDEFGHIJ"
        col_index = valid_cols.index(col)

        # Possible surrounding row and column offsets (-1, 0, 1)
        row_offsets = [-1, 0, 1]
        col_offsets = [-1, 0, 1]

        # Iterate over each combination of row and column offsets
        for r_offset in row_offsets:
            for c_offset in col_offsets:
                #Skip the digaonals and the center
                if abs(r_offset) ^ abs(c_offset) == False:
                    continue

                # Calculate the new row and column
                new_row = row + r_offset
                new_col_index = col_index + c_offset

                # Check if the new row and column are valid and append to self.near[]
                if 1 <= new_row <= 10 and 0 <= new_col_index < len(valid_cols):
                    new_col = valid_cols[new_col_index]
                    self.near.append(f"{new_col}{new_row}")
    
    # returns a coordinate to attack based on the difficulty of the ai
    def attack(self):
        diff = self.difficulty
        match self.difficulty:
            #finds a coordinate to shoot at based on the difficulty of it ai
            case 0:
                #returns a random coordinate
                return self.get_random_coordinate()
            case 1:
                if len(self.near) > 0:
                    coor = self.near[0]
                    self.near = self.near[1:]
                    return coor
                return self.get_random_coordinate()
            case 2:
                #returns the coordinate of the first item in the enemy coordinates
                coord = self.enemy_coordinates[0]
                self.enemy_coordinates = self.enemy_coordinates[1:]
                return string.ascii_uppercase[coord[1]]+str(coord[0] + 1)
            
    def handleHit(self, coor, sunk):
        if self.difficulty == 1:
            if sunk:
                #clear self.near
                self.near = []
            else:
                #handle surrounding coor
                self.get_surrounding_coordinates(coor)
                print("I am handling coordinates")
                print(self.near)




def main():
    ai = Ai(1, None)
    coord = ai.get_random_coordinate()
    print(coord)

    ai.get_surrounding_coordinates(coord)
    print(ai.near)


if __name__ == "__main__":
    main()




