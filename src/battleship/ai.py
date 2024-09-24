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

import random
import string

class Ai:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        if(difficulty == 1):
            self.hits = []
            self.near = []
        elif(difficulty == 2):
            self.enemy_coordinates = []

    # Returns as a string 
    def get_random_coordinate(self):
        col = random.choice(string.ascii_uppercase[:10])
        row = str(random.randint(1,10))
        
        return col+row

    def get_surrounding_coordinates(self, coordinate):

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
                # Skip the original coordinate (0,0 offset)
                if r_offset == 0 and c_offset == 0:
                    continue

                # Calculate the new row and column
                new_row = row + r_offset
                new_col_index = col_index + c_offset

                # Check if the new row and column are valid
                if 1 <= new_row <= 10 and 0 <= new_col_index < len(valid_cols):
                    new_col = valid_cols[new_col_index]
                    self.near.append(f"{new_col}{new_row}")




def main():
    ai = Ai(1)
    coord = ai.get_random_coordinate()
    print(coord)

    ai.get_surrounding_coordinates(coord)
    print(ai.near)


if __name__ == "__main__":
    main()





