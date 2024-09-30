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

import random #import for random
import string #import for strings
from player import Player #import player
from ship import Ship #import ship
from exceptions import AlreadyFiredError #import errors

class Ai(Player): #Ai class that is a subclass of the player class
    def __init__(self, difficulty, opponent, ships: list[Ship] = None) -> None: #constructor which takes a diffculty and opponent. Also handles ship creation.
        self.difficulty = difficulty #difficulty of the ai
        self._name = "AI" # name attribute for printing player info
        self.enemy_coordinates = [] #coordinates of the oposing players ships
        
        # hits[] = coordinates of hits
        # near[] = valid coordinates surrounding the most recent hit
        if(difficulty == 1): #if difficulty is 1
            self.hits = [] #create hits array
            self.near = [] #create near array
        elif(difficulty == 2): #if difficulty is 2
            #for each coordinate in each ship in the opponent's list of ships, we add the coordinate to self._enemy_coordinates
            for ship in opponent.ships: #iterate over opponent ships
                for coor in ship.hull: #iterate over the opposing coordinates
                    temp = coor[:2] #slice the coordinates as needed
                    self.enemy_coordinates.append(temp) #append the slices coordinate
                    
        if ships is None: #if no ships
            self._ships = [] #set ships to empty list
        else: #else
            self._ships: list[Ship] = ships #set ships to list[ship] = ships

        #hold the state of the board. the i,j entry of the board represents the if a shot has been fired at coordinate i,j.
        self._board_state: list[list[bool]] = [ [ False for _ in range(10) ] for _ in range(10) ] #note that this contains NO information about whether that was a hit or a miss, that information is tracked by each ship.

        self._num_alive_ships: int = len(self._ships) #set the number of alive ships using len

    # Returns a string literal of a random coordinate on the board
    def get_random_coordinate(self): #function to get random coordinate
        col = random.choice(string.ascii_uppercase[:10]) #take a random choice of ascii letters in range
        row = str(random.randint(1,10)) #get a random integer in range
        
        return col+row #return col+row

    def get_surrounding_coordinates(self, coordinate): #function to get surrounding coordinates

        col = coordinate[0] #column is letter
        row = int(coordinate[1:]) #row is the rest

        valid_cols = "ABCDEFGHIJ"  # Define valid columns (A-J)
        col_index = valid_cols.index(col) #get column index

        row_offsets = [-1, 0, 1] # Possible surrounding row and column offsets (-1, 0, 1)
        col_offsets = [-1, 0, 1] # Possible surrounding row and column offsets (-1, 0, 1)

        # Iterate over each combination of row and column offsets
        for r_offset in row_offsets: #iterate over rows
            for c_offset in col_offsets: #iterate over cols
                if abs(r_offset) ^ abs(c_offset) == False: #Skip the digaonals and the center
                    continue #continue

                # Calculate the new row and column
                new_row = row + r_offset #calc new row
                new_col_index = col_index + c_offset #calc new col

                # Check if the new row and column are valid
                if 1 <= new_row <= 10 and 0 <= new_col_index < len(valid_cols): #if statement to check validity
                    new_col = valid_cols[new_col_index] #seet new col
                    self.near.append(f"{new_col}{new_row}") #append new str
    
    #returns a coordinate to attack based on the difficulty of the ai
    def attack(self): #define attack function
        diff = self.difficulty #extract difficulty
        match self.difficulty: #case match block
            #finds a coordinate to shoot at based on the difficulty of it ai
            case 0: #case 0
                return self.get_random_coordinate()  #returns a random coordinate
            case 1: # case 1
                if len(self.near) > 0: #if nearby coords
                    coor = self.near[0] #extract first index
                    self.near = self.near[1:] #remove first index
                    return coor #return that coordinate
                return self.get_random_coordinate() #return random coordinate
            case 2: # case 2
                #returns the coordinate of the first item in the enemy coordinates
                coord = self.enemy_coordinates[0] #get first enemy coordinate
                self.enemy_coordinates = self.enemy_coordinates[1:] #remove first enemy coordinate
                return string.ascii_uppercase[coord[1]]+str(coord[0] + 1) #return coordinate
            
    def handleHit(self, coor, sunk): #function to handle hits
        if self.difficulty == 1: #if difficulty 1
            if sunk: # if sunk
                self.near = [] #clear self.near
            else: #else
                #handle surrounding coor
                self.get_surrounding_coordinates(coor) # get surrounding coordinates
                print("I am handling coordinates") #handling coordinates
                print(self.near) #print nearby coordinates





