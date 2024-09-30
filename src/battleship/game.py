"""
Name of program: game.py
Description: Class to control game and game state.
Inputs: None
Outputs: None
Other sources for code: N/A
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le
Authors: Steve Gan, Sean Hammell, Jacob Leehy, Mario Simental, Matthew Sullivan
Creation date: 09/11/24
"""


import os      # import os for screen clearing.
import random  # import random library for random ai functionality.
import string  # import string for enhanced string functionality.

# https://docs.python.org/3/library/getpass.html#getpass.getpass
from getpass import getpass  # import getpass to work with passwords.

from ai import Ai          # import Ai class.
from player import Player  # import Player class.
from ship import Ship      # import Ship class.

# import custom exceptions for ship length, coordinates, duplicate firing, and special shots.
from exceptions import InvalidShipLengthError, InvalidCoordinatesError, AlreadyFiredError, EmptySpecialShotsError

class Game:
    """
    For managing the overall state of a game of battleship as well as interactions between the players.
    """

    def __init__(self, num_ships: int) -> None:
        """Initialize Player objects, gets their password for the game, and has them input their ship locations"""
        
        #print welcome message.
        print('================\nWelcome Player 1\n================')
        
        #get player name.
        player_one_name: str = input('What\'s your name? ')

        #get player password.
        self._player_one_pass: str = getpass('Enter your password: ') 

        #create player 1 object.
        self._player_one: Player = Game._build_player(player_one_name, num_ships)

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')
        
        #print welcome message
        print('================\nWelcome Player 2\n================')
        
        #get player name.
        player_two_name: str = input('What\'s your name? Enter \'ai\' to play against an ai: ')
        # if the second player is not Ai.
        if player_two_name.lower() != 'ai':
            self._player_two_pass: str = getpass('Enter your password: ')
            self._player_two: Player = Game._build_player(player_two_name, num_ships)

            # prompt for number of special shots to be played with
            print('================\nSetup\n================')
            # until the user enters a valid number of special shots.
            while True:
                try:
                    # try to get a valid number of special shots from the user.
                    self._num_special_shots: int = int(input('How many special shots (3x3) would you like to play with (0-999): '))
                except ValueError:
                    # except a value error and prompt the user again.
                    print('Please input a number.')
                    continue

                # if the number is outside the range [0, 999].
                if not 0 <= self._num_special_shots <= 999:
                    # prompt the user agina.
                    print('Please input a number between 0 and 999.')
                    continue

                break

            # set the number of special shots for both players.
            self._player_one.set_special_shots(self._num_special_shots)
            self._player_two.set_special_shots(self._num_special_shots)
        # if the second player is Ai.
        else:
            # prompt the user for the Ai difficulty level.
            difficulty = int(input('Enter ai difficulty level. (0 - easy, 1 - medium, 2 - hard): '))
            # if the value is not in the range [0, 3].
            if not 0 <= difficulty <= 3:
                # raise a value error
                raise ValueError
            # otherwise create the Ai player
            self._player_two: Ai = Game._build_ai_player(player_two_name, num_ships, self._player_one, difficulty)

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _build_ai_player(name: str, num_ships: int, opponent: Player, difficulty=0):
        """
        Builds an AI player with a random name, number of ships, and difficulty level.
        """
        def generate_random_coordinate():
            """
            Generates a random coordinate.
            """
            letter = random.choice(string.ascii_uppercase[:10])  # picks a random letter from A to J
            number = random.randint(1, 9)                        # picks a random number between 1 and 9
            return f"{letter}{number}"                           # return the coordinate
        
        def get_neighbors(coordinate, distance=1):
            """
            Get the coordinates orthogonal to the specified coordinate.
            """
            letter = coordinate[0]        # extract the letter from the coordinate
            number = int(coordinate[1:])  # extract the number from the coordinate

            letters = string.ascii_uppercase[:10]  # get the first ten letters of the alphabet
            letter_idx = letters.index(letter)     # get the index of the coordinate letter

            neighbors = []  # create a list to store neighbors of the coordinate

            for i in range(1, distance + 1):                                # horizontal neighbors
                if letter_idx - i >= 0:                                     # left neighbor
                    neighbors.append(f"{letters[letter_idx - i]}{number}")  # add the neighbor to the list
                if letter_idx + i < 10:                                     # right neighbor
                    neighbors.append(f"{letters[letter_idx + i]}{number}")  # add the neighbor to the list

            for i in range(1, distance + 1):                   # vertical neighbors
                if number - i >= 1:                            # downward neighbor
                    neighbors.append(f"{letter}{number - i}")  # add the neighbor to the list
                if number + i <= 9:                            # upward neighbor
                    neighbors.append(f"{letter}{number + i}")  # add the neighbor to the list

            return neighbors  # return the list of neighbors

        def generate_random_neighbor(coordinate, distance=1):
            """
            Get a randomly chosen coordinate orthogonol to the specified coordinate.
            """
            neighbors = get_neighbors(coordinate, distance)  # get all neighbors of the specified coordinate.
            if neighbors:                                    # if the coordinate has neighbors.
                return random.choice(neighbors)              # return a random neighbor.
            return None                                      # otherwise, return None

        # create an Ai player
        player : Ai = Ai(difficulty, opponent)
        # Initialize the ship length to 0
        ship_length: int = 0

        for _ in range(num_ships):  # for each ship
            ship_length += 1        # increment the ship length from the previous ship

            while True:  # until there is a valid ship to place
                try:
                    if ship_length == 1:                                         # if the ship length is 1, only ask for one coordinate.
                        coord_input = generate_random_coordinate()               # get a random coordinate
                        start_coord = Game._parse_coordinate(coord_input)        # convert the input to a tuple of ints (row, col)
                        end_coord = start_coord                                  # since it's a 1-length ship, start and end are the same
                    else:                                                                             # if the ship length is greater than 1
                        start_coord_input = generate_random_coordinate()                              # get a random coordinate
                        start_coord = Game._parse_coordinate(start_coord_input)                       # convert the input to a tuple of ints (row, col)
                        end_coord_input = generate_random_neighbor(start_coord_input, ship_length-1)  # get the ending coordinate for the ship
                        end_coord = Game._parse_coordinate(end_coord_input)                           # convert the input to a tuple of ints (row, col)

                    ship: Ship = Ship(ship_length, start_coord, end_coord)  # create a Ship object with the given coordinates
                    
                    try:
                        player.add_ship(ship)  # add the ship to the player
            
                    except ValueError:                                                    # if the ship intersects another ship
                        print('This placement intersects another ship, please try again.')# ask for coordinates again
                        continue

                    break  # break out of the loop

                except (InvalidShipLengthError, InvalidCoordinatesError) as e:  # if the ship or coordinates are invalid
                    print(f'[ERROR] {e} Please try again.')                     # ask for coordinates again
                    continue

        return player  # return the Ai player

    @staticmethod
    def _build_player(name: str, num_ships: int) -> Player:
        """
        Talks to the user and initialize a player object.
        """
        # Create a Player object with the given name
        player: Player = Player(name)
        # Initialize the ship length to 0
        ship_length: int = 0
        # Ask the user for the coordinates of each ship
        for _ in range(num_ships):
            # increment the ship length by one from the previous ship
            ship_length += 1

            # until receiving a valid ship placement
            while True:
                # display the player's private board
                player.display_board_private()

                try:
                    # If the ship length is 1, only ask for one coordinate
                    if ship_length == 1:
                        # prompt the user for a coordinate
                        coord_input = input(f'Enter coordinate for a ship that is {ship_length} long (e.g., A1 or A,1): ').replace(' ', '').upper()
                        # Convert the input to a tuple of ints (row, col)
                        start_coord = Game._parse_coordinate(coord_input)
                        # Since it's a 1-length ship, start and end are the same
                        end_coord = start_coord
                    # if the ship length is greater than one
                    else:
                        # prompt the user for a starting coordinate
                        start_coord_input = input(f'Enter starting coordinate for a ship that is {ship_length} long (e.g., A1 or A,1): ').replace(' ', '').upper()
                        # Convert the input to a tuple of ints (row, col)
                        start_coord = Game._parse_coordinate(start_coord_input)

                        # Get the ending coordinate for the ship
                        end_coord_input = input(f'Enter ending coordinate for the ship (e.g., A1 or A,1): ').replace(' ', '').upper()
                        # Convert the input to a tuple of ints (row, col)
                        end_coord = Game._parse_coordinate(end_coord_input)

                    # Create a Ship object with the given coordinates
                    ship: Ship = Ship(ship_length, start_coord, end_coord)
                    
                    try:
                        # add the ship to the player's board
                        player.add_ship(ship)
            
                    except ValueError:
                        # If the ship intersects another ship, ask for coordinates again
                        print('This placement intersects another ship, please try again.')
                        continue

                    break

                except (InvalidShipLengthError, InvalidCoordinatesError) as e:
                    # If the ship length is invalid or the coordinates are invalid, ask for coordinates again
                    print(f'[ERROR] {e} Please try again.')
                    continue

        # return the Player object
        return player

    @staticmethod
    def _parse_coordinate(input_str: str) -> tuple[int, int]:
        """Converts a string in 'A1' or 'A,1' format to a tuple of ints (row, col)"""
        # Remove spaces and normalize to uppercase
        input_str = input_str.replace(' ', '').upper()  

        # Allow either "A1" or "A,1" format for input
        if ',' in input_str:  # Format is A,1
            col_str, row_str = input_str.split(',')
        else:  # Format is A1
            col_str, row_str = input_str[0], input_str[1:]

        # Validate the row and column
        if not row_str.isdigit() or len(row_str) > 2:
            raise InvalidCoordinatesError(f"Invalid row number '{row_str}'. Please use a number between 1 and 10.")

        row = int(row_str) - 1  # Convert row to 0-indexed
        col_num: int = "ABCDEFGHIJ".find(col_str)
        # Check if the column is a valid letter and the row is between 1 and 10
        if col_num == -1 or not (0 <= row <= 9):
            # If the column is not a valid letter or the row is not between 1 and 10
            raise InvalidCoordinatesError("Coordinate not on board. Please use a valid format (e.g., A1 or A,1).")

        # return the coordinate
        return (row, col_num)

    #password checking loop
    def _check_pass(self, player: Player) -> None:
        # Get the correct password for the player
        player_pass: str = self._player_one_pass if player is self._player_one else self._player_two_pass

        while True:
            # Get the player's password
            check: str = getpass(f'[{player.name}]: Enter your password: ')
            # Check if the password is correct
            if check == player_pass:
                # break out of the loop if the password is correct
                break

            # let the user know the password was incorrect
            print('Incorrect! Please try again.')

    def loop(self) -> None:
        """Main gameplay loop. Displays menu and executes choices."""
        # keep track of the number of turns played
        turn_count: int = 0 
        # start with current player as player 1 
        current_player: Player = self._player_one 
        # start with opponent player as player 2
        if isinstance(self._player_two, Ai):
            # set the opponent player as Ai
            opponent_player: Ai = self._player_two
        else:
            # set the opponent player as a human
            opponent_player: Player = self._player_two

        while True: #loop infinitely! (Until break is called)
            # if the player is human
            if not isinstance(current_player, Ai):
                # check the password
                self._check_pass(current_player)
        
            while True:
                # if the player is Ai
                if isinstance(current_player, Ai):
                    rawcoor = current_player.attack()  # get the Ai attack coordinate
                    coor = Game._parse_coordinate(rawcoor)  # parse the coordinate
                    try:
                        temp = opponent_player.num_alive_ships  # get the number of alive opponent ships
                        if opponent_player.take_hit(coor):  # play the attack
                            print('Your opponent hit you!')  # if the attack hit
                            current_player.handleHit(rawcoor, temp != opponent_player.num_alive_ships)  # handle any post-attack logic
                        else:  # other wise
                            print('Your opponent missed you!')  # move along
                        input('Press ENTER to continue')  # prompt for Enter to continue
                        break
                    except (AlreadyFiredError, InvalidCoordinatesError) as e:
                        continue  # handle duplicate attack and invalid coordinate errors
                else: 
                    print(f'================\nTURN {turn_count}\n================')
                    # if the current player has special shots left
                    if current_player.num_special_shots > 0:
                        # print the player's options
                        print(f'[0] CHECK YOUR BOARD\n[1] CHECK OPPONENTS BOARD\n[2] FIRE\n[3] FIRE SPECIAL SHOT ({current_player.num_special_shots}/{self._num_special_shots})\n================')
                        valid_choices = [0, 1, 2, 3]
                    # if the current player does not have special shots left
                    else:
                         # print the player's options
                         print('[0] CHECK YOUR BOARD\n[1] CHECK OPPONENTS BOARD\n[2] FIRE\n================')
                         valid_choices = [0, 1, 2] 
                    try:
                        # prompt the user for an action
                        player_input: int = int(input('What would you like to do?: '))
                        
                        # Check if the input is valid based on available choices
                        if player_input not in valid_choices:
                            raise ValueError
                        
                    except ValueError:
                        # if the input was invalid prompt the user again
                        print('Invalid input, please choose off of the menu.')
                        continue

                    match player_input:
                        case 0:
                            # Display the current player's board
                            current_player.display_board_private()
                        case 1:
                            # Display the opponent's board
                            #opponent_player.display_board_private()
                            opponent_player.display_board_public()
                        case 2:
                            try:
                                # Get the coordinate to fire at
                                opponent_player.display_board_public()
                                coord_input = input(f'Enter a coordinate to fire (e.g., A1 or A,1): ').replace(' ', '').upper()
                                # Convert the input to a tuple of ints (row, col)
                                coord: tuple[int, int] = Game._parse_coordinate(coord_input)
                                
                                # Check if the shot hit a ship
                                if opponent_player.take_hit(coord):
                                    print('Hit!') #print hit ahd call handleHit if it is a hit
                                else:
                                    print('Miss!') #print miss if the shot is a miss
                                # Display the opponent's board after the shot
                                opponent_player.display_board_public()
                                input('Press ENTER to continue')
                                break
                                    
                            except (AlreadyFiredError, InvalidCoordinatesError) as e: #error if already fired upon coordinate or if invalid coordinate
                                print(e)
                        case 3:
                            try:
                                # Get the coordinate to fire at
                                opponent_player.display_board_public()
                                coord_input = input(f'Enter a coordinate to fire a special shot (e.g., A1 or A,1): ').replace(' ', '').upper()
                                # Convert the input to a tuple of ints (row, col)
                                coord: tuple[int, int] = Game._parse_coordinate(coord_input)
                                
                                if not current_player.num_special_shots > 0:
                                    raise EmptySpecialShotsError("You have no special shots remaining.")
                            
                                # Check if the shot hit a ship
                                print('Hit!' if opponent_player.take_special_hit(coord) else 'Miss!')
                                current_player.num_special_shots -= 1
                                # Display the opponent's board after the shot
                                opponent_player.display_board_public()
                                input('Press ENTER to continue')
                                break
                                    
                            except (AlreadyFiredError, InvalidCoordinatesError, EmptySpecialShotsError) as e:
                                print(e)  # handle an invalid coordinate, duplicate attack, or empty special shots

            #check if either p1 or p2's ships are all destroyed
            #(possibly take this block and put it into its own function)
            if opponent_player.num_alive_ships == 0:
                print(f'================\n {current_player.name} Wins!\n================')
                break #leave the while loop

            #clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            #swap current player with opponent player
            temp_player: Player = current_player
            #  swap the players
            current_player = opponent_player
            # swap the opponents
            opponent_player = temp_player
            # increment the turn count
            turn_count += 1
