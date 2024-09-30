from ship import Ship
from exceptions import AlreadyFiredError

class Player:
    """
    Manages the state of a players board, as well as displaying said board in various contexts.
    """

    def __init__(self, name: str, ships: list[Ship] = None) -> None:
       
        self._name: str = name  # record the Player's name
        self.num_special_shots: int = 0  # record the number of special shots the Player has

        if ships is None:  # if no ships were passed in
            self._ships = []  # initialize ships to an empty list
        else:  # otherwise
            self._ships: list[Ship] = ships  # record the list of ships

        #hold the state of the board. the i,j entry of the board represents the if a shot has been fired at coordinate i,j.
        #note that this contains NO information about whether that was a hit or a miss, that information is tracked by each ship.
        self._board_state: list[list[bool]] = [ [ False for _ in range(10) ] for _ in range(10) ]

        self._num_alive_ships: int = len(self._ships)  # all of the Player's ships are alive
    
    @property #returns the name of the player
    def name(self) -> str:
        return self._name

    @property #returns the number of ships of the player
    def num_ships(self) -> int:
        return len(self._ships)

    @property #returns the number of ships still alive of the player
    def num_alive_ships(self) -> int:
        return self._num_alive_ships

    @property #returns the number of ships sunk of the player
    def num_sunk_ships(self) -> int:
        return self.num_ships - self.num_alive_ships
    
    @property #returns the location and status of the ships of the player
    def ships(self):
        return self._ships 

    def take_hit(self, coordinate: tuple[int, int]) -> bool:
        """Take a hit at the given coordinate and update the board state."""
        
        if self._board_state[coordinate[0]][coordinate[1]]:  # if the coordinate has already been hit
            raise AlreadyFiredError("You have already fired on this coordinate.")  # raise an error

        self._board_state[coordinate[0]][coordinate[1]] = True  # record the hit

        for ship in self._ships:
            # Check if the hit is on any ship
            for hull in ship.hull:
                # If the hit is on the ship
                if hull[:2] == coordinate:
                    # Mark the hit on the ship
                    ship.take_hit(coordinate)
                    # Check if the ship is sunk
                    if ship.sunk:
                        # Decrement the number of alive ships
                        self._num_alive_ships -= 1
                    return True  # return that the shot was a hit
        return False  # return that the shot was a miss

    def take_special_hit(self, coordinate: tuple[int, int]) -> bool:
        """
        Handle a special 3x3 shot centered at `center_coord`.
        The 3x3 shot affects the center and all valid adjacent cells.
        """

        row, col = coordinate  # parse the coordinate

        if self._board_state[row][col]:  # if the coordinate has already been hit
            raise AlreadyFiredError("You have already fired on this coordinate.")  # raise an error

        self._board_state[row][col] = True  # record the hit

        hit_anything = False  # initialize the hit flag to False

        # Define the range for 3x3 area
        # Reminder range upper is not inclusive hence + 2
        for i in range(max(0, row - 1), min(10, row + 2)):  # Ensures rows stay within bounds
            for j in range(max(0, col - 1), min(10, col + 2)):  # Ensures columns stay within bounds

                # Mark this coordinate as fired upon
                self._board_state[i][j] = True

                # Check if any ship is hit
                for ship in self._ships:
                    # Check if the hit is on any ship
                    for hull in ship.hull:
                        # If the hit is on the ship
                        if hull[:2] == (i,j):
                            # Mark the hit on the ship
                            ship.take_hit((i,j))
                            # Check if the ship is sunk
                            if ship.sunk:
                                # Decrement the number of alive ships
                                self._num_alive_ships -= 1
                            hit_anything = True

        return hit_anything  # return if the special shot hit anything
    
    def set_special_shots(self, num: int) -> None:
        """
        Set the number of special shots.
        """
        self.num_special_shots = num

    def _get_cell_state(self, i: int, j: int, private: bool) -> str:
        """Serve as a helper method to get the state of each cell for private and public boards."""
        # Check if the cell is part of any ship
        for ship in self._ships:
            # Check if the cell is part of the ship
            for x, y, hit in ship.hull:
                # If the cell is part of the ship
                if (i, j) == (x, y):
                    # Check if the ship is sunk
                    if ship.sunk:
                        return '@' # Sunken ship
                    elif hit:
                        return 'X' # Hit ship
                    elif private:
                        return 'S' # Ship but not hit (only visible in private view)

        # No ship in this cell
        if self._board_state[i][j]:
            return 'O' # Shot at, but missed
        return '~' # Unshot cell

    def display_board_private(self) -> None:
        """Display the state of the board to the player."""
        print('    A B C D E F G H I J ') # Print top border labels.
        print('  +' + '-' * 21 + '+') # Top border

        for i in range(10):  # for each row
            row: list[str] = [self._get_cell_state(i, j, private=True) for j in range(10)]  # get the cell states in the row
            print(f"{i+1}{' ' if i+1 != 10 else ''}| {' '.join(row)} |") # Board with side borders & side border numbers
        
        print('  +' + '-' * 21 + '+') # Bottom border

    def display_board_public(self) -> None:
        """Display the state of the board to the opponent."""
        print('    A B C D E F G H I J ') # Print top border labels.
        print(' +' + '-' * 21 + '+') # Top border

        for i in range(10):  # for each row
            row: list[str] = [self._get_cell_state(i, j, private=False) for j in range(10)]  # get the cell states in the row
            print(f"{i+1}{' ' if i+1 != 10 else ''}| {' '.join(row)} |") # Board with side borders & side boarder numbers

        print('  +' + '-' * 21 + '+') # Bottom border

    def add_ship(self, ship: Ship) -> None:
        
        #validate placement.
        for other_ship in self._ships:
            # Check if the ship intersects with any other ship
            for other_x, other_y, _ in other_ship.hull:
                for x, y, _ in ship.hull:
                    #  If the coordinate of the ship is the same as the coordinate of another ship
                    if (x,y) == (other_x, other_y):
                        raise ValueError('Placement intersects another ship.')  # raise an error

        self._ships.append(ship)  # add the ship to the list of ships
        self._num_alive_ships += 1  # increment the number of alive ships
