'''
Program Name: ai.py
Description: Class for an Ai player with three difficulty levels that a human
             player may choose to play against.
Inputs: Difficulty, opponent, and list of ships
Output: Attacks
Code Sources: None
Authors: Steve Gan, Sean Hammell, Jacob Leehy, Mario Simental, Matthew Sullivan
Creation Date: 9/23/24
'''

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

import random #import for random
import string #import for string
from player import Player #import for player
from ship import Ship #import for ship
from exceptions import AlreadyFiredError #import exceptions

class Ai(Player): #ai player class - subclass of player - responsible for managing ai players
    def __init__(self, difficulty, opponent, ships: list[Ship] = None) -> None: #constructor - takes difficulty, opponent, and sets up ships
        self.difficulty = difficulty #difficulty of the ai
        self.enemy_coordinates = [] #coordinates of the oposing players ships
        self._name = "AI" #initialize name for end card

        # For medium difficulty, the AI needs to track the most recent hit, and the surrounding coordinates of the hit
        # self.near is an array of the surrounding coordinates and will be used for moves after there is a hit
        if(difficulty == 1): # if difficulty 1
            self.hits = [] #create hits
            self.near = [] #create near
        elif(difficulty == 2): # if difficulty 2
            #for each coordinate in each ship in the opponent's list of ships, we add the coordinate to self._enemy_coordinates
            for ship in opponent.ships: #iterate over opponent ships
                for coor in ship.hull: #iterate over hulls
                    temp = coor[:2] # slicee hulls
                    self.enemy_coordinates.append(temp) #append temp coords
        
        # If ships is None, set self._ships to an empty list            
        if ships is None: # if no ships
            self._ships = [] #create ships list
        else: # else
            self._ships: list[Ship] = ships #set list[ship] to ships

        #hold the state of the board. the i,j entry of the board represents the if a shot has been fired at coordinate i,j.
        #note that this contains NO information about whether that was a hit or a miss, that information is tracked by each ship.
        self._board_state: list[list[bool]] = [ [ False for _ in range(10) ] for _ in range(10) ]

        self._num_alive_ships: int = len(self._ships) #set num of alive ships with len

    # Returns a string literal of a randomly generated coordinate
    def get_random_coordinate(self): #gets random coord
        col = random.choice(string.ascii_uppercase[:10]) #gets random col
        row = str(random.randint(1,10)) #gets random row
        
        return col+row #return col and row

    # Populates self.near[] after a ship is hit with valid surrounding coordinates, excluding diagonals
    def get_surrounding_coordinates(self, coordinate): #gets surrounding coordinates

        # Parse and cast coordinate string to extract column and row
        col = coordinate[0] #col is letter
        row = int(coordinate[1:]) #row is everything else

        # Define valid columns (A-J)
        valid_cols = "ABCDEFGHIJ" #valid cols
        col_index = valid_cols.index(col) #set col index

        # Possible surrounding row and column offsets (-1, 0, 1)
        row_offsets = [-1, 0, 1] #possible row offsets
        col_offsets = [-1, 0, 1] #possible col offsets

        # Iterate over each combination of row and column offsets
        for r_offset in row_offsets: #iterate over row off
            for c_offset in col_offsets: #iterate over col off
                #Skip the digaonals and the center
                if abs(r_offset) ^ abs(c_offset) == False: #skip diag and center
                    continue #continue

                # Calculate the new row and column
                new_row = row + r_offset #new row
                new_col_index = col_index + c_offset #new col

                # Check if the new row and column are valid and append to self.near[]
                if 1 <= new_row <= 10 and 0 <= new_col_index < len(valid_cols): #if valid
                    new_col = valid_cols[new_col_index] #new col
                    self.near.append(f"{new_col}{new_row}") #add to near
    
    # returns a coordinate to attack based on the difficulty of the ai
    def attack(self): #def attack function
        diff = self.difficulty #extract difficulty
        match self.difficulty: #case match with difficulty
            #finds a coordinate to shoot at based on the difficulty of it ai
            case 0: #case 0
                #returns a random coordinate
                return self.get_random_coordinate() #return random coord
            case 1: #case 1
                if len(self.near) > 0: # if something in near
                    coor = self.near[0] # get first element
                    self.near = self.near[1:] #remove first element
                    return coor #return coord
                return self.get_random_coordinate() #get random coord
            case 2: #case 2
                #returns the coordinate of the first item in the enemy coordinates
                coord = self.enemy_coordinates[0] #extract first enemy coord
                self.enemy_coordinates = self.enemy_coordinates[1:] #remove first enemy coord
                return string.ascii_uppercase[coord[1]]+str(coord[0] + 1) #return ascii
            
    def handleHit(self, coor, sunk): #function to handle hits
        if self.difficulty == 1: #if difficulty is 1
            if sunk: # if sunk
                #clear self.near
                self.near = [] #clear nearby ships
            else: #else
                #handle surrounding coor
                self.get_surrounding_coordinates(coor) #get surrounding coords
                print("I am handling coordinates") #print message
                print(self.near) #print near




def main():
    ai = Ai(1, None)
    coord = ai.get_random_coordinate()
    print(coord)

    ai.get_surrounding_coordinates(coord)
    print(ai.near)


if __name__ == "__main__":
    main()




