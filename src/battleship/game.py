"""
Name of program: game.py
Description: Class to control game and game state.
Inputs: None
Outputs: None
Other sources for code: N/A
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le
Creation date: 09/11/24
"""

#used for clearing the screen, as we need to know what is we are on to send the proper control character.
import os

#used for getting passwords: https://docs.python.org/3/library/getpass.html#getpass.getpass
from getpass import getpass

#import player class.
from player import Player
from ai import Ai
import random
import string

#import ship class.
from ship import Ship

#import exception that denotes invalid ship length.
from exceptions import InvalidShipLengthError, InvalidCoordinatesError, AlreadyFiredError

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
        if player_two_name.lower() != 'ai':
            #get player password.
            self._player_two_pass: str = getpass('Enter your password: ')
            #build player 2 object.
            self._player_two: Player = Game._build_player(player_two_name, num_ships)
            # prompt for number of special shots to be played with

            print('================\nSetup\n================')
            while True:
                try:
                    self._num_special_shots: int = int(input('How many special shots (3x3) would you like to play with (0-999): '))
                except ValueError:
                    print('Please input a number.')
                    continue

                if not 0 <= self._num_special_shots <= 999:
                    print('Please input a number between 0 and 999.')
                    continue

                break
        else:
            difficulty = int(input('Enter ai difficulty level. (0 - easy, 1 - medium, 2 - hard): '))
            if not 0 <= difficulty <= 3:
                raise ValueError
            self._player_two: Ai = Game._build_ai_player(player_two_name, num_ships, difficulty)
            #self._player_two_pass: str = ""

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _build_ai_player(name: str, num_ships: int, difficulty=0):
        def generate_random_coordinate():
            letter = random.choice(string.ascii_uppercase[:10])  # Picks a random letter from A to J
            number = random.randint(1, 9)  # Picks a random number between 1 and 9
            return f"{letter}{number}"
        
        def get_neighbors(coordinate, distance=1):
            # Extract the letter and number from the coordinate
            letter = coordinate[0]
            number = int(coordinate[1:])

            # Get all possible letters and numbers
            letters = string.ascii_uppercase[:10]
            letter_idx = letters.index(letter)

            # Store valid neighbors within the specified distance
            neighbors = []

            # Horizontal neighbors
            for i in range(1, distance + 1):
                if letter_idx - i >= 0:  # Left neighbor
                    neighbors.append(f"{letters[letter_idx - i]}{number}")
                if letter_idx + i < 10:  # Right neighbor
                    neighbors.append(f"{letters[letter_idx + i]}{number}")

            # Vertical neighbors
            for i in range(1, distance + 1):
                if number - i >= 1:  # Downward neighbor
                    neighbors.append(f"{letter}{number - i}")
                if number + i <= 9:  # Upward neighbor
                    neighbors.append(f"{letter}{number + i}")

            return neighbors

        def generate_random_neighbor(coordinate, distance=1):
            neighbors = get_neighbors(coordinate, distance)
            if neighbors:
                return random.choice(neighbors)
            return None

        player : Ai = Ai(difficulty)
        # Initialize the ship length to 0
        ship_length: int = 0
        # Ask the user for the coordinates of each ship
        for _ in range(num_ships):
            
            ship_length += 1

            while True:

                #player.display_board_private()

                try:
                    # If the ship length is 1, only ask for one coordinate
                    if ship_length == 1:
                        coord_input = generate_random_coordinate()
                        # Convert the input to a tuple of ints (row, col)
                        start_coord = Game._parse_coordinate(coord_input)
                        # Since it's a 1-length ship, start and end are the same
                        end_coord = start_coord  
                    else:
                        start_coord_input = generate_random_coordinate()
                        # Convert the input to a tuple of ints (row, col)
                        start_coord = Game._parse_coordinate(start_coord_input)

                        # Get the ending coordinate for the ship
                        end_coord_input = generate_random_neighbor(start_coord_input, ship_length-1)
                        # Convert the input to a tuple of ints (row, col)
                        end_coord = Game._parse_coordinate(end_coord_input)

                    # Create a Ship object with the given coordinates
                    ship: Ship = Ship(ship_length, start_coord, end_coord)
                    
                    try:
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

        return player

    @staticmethod
    def _build_player(name: str, num_ships: int) -> Player:
        """Talk to the user and initialize a player object."""
        # Create a Player object with the given name
        player: Player = Player(name)
        # Initialize the ship length to 0
        ship_length: int = 0
        # Ask the user for the coordinates of each ship
        for _ in range(num_ships):
            
            ship_length += 1

            while True:

                player.display_board_private()

                try:
                    # If the ship length is 1, only ask for one coordinate
                    if ship_length == 1:
                        coord_input = input(f'Enter coordinate for a ship that is {ship_length} long (e.g., A1 or A,1): ').replace(' ', '').upper()
                        # Convert the input to a tuple of ints (row, col)
                        start_coord = Game._parse_coordinate(coord_input)
                        # Since it's a 1-length ship, start and end are the same
                        end_coord = start_coord  
                    else:
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
                break

            print('Incorrect! Please try again.')

    def loop(self) -> None:
        """Main gameplay loop. Displays menu and executes choices."""
        turn_count: int = 0 
        #start with player 1
        current_player: Player = self._player_one 
        # start with player 2
        if isinstance(self._player_two, Ai):
            opponent_player: Ai = self._player_two
        else:
            opponent_player: Player = self._player_two

        while True: #loop infinitely! (Until break is called)
            """
            if isinstance(current_player, Ai):
                attack_coord = current_player.attack
                enemy_ships_pre_attack = opponent_player._num_alive_ships
                hit = opponent_player.take_hit(attack_coord)
                if hit:
                    if opponent_player._num_alive_ships < enemy_ships_pre_attack:
                        current_player.update_after_attack(attack_coord, sink)
                    else:
                        current_player.update_after_attack(attack_coord, hit)
            else:
                everything that's already written for a human player

            still need to clear the screen and switch players at the end
            """
            #password check
            if not isinstance(current_player, Ai):
                self._check_pass(current_player)
        
            while True:
                #handle turn
                if isinstance(current_player, Ai):
                    coor = Game._parse_coordinate(current_player.attack())
                    try:
                        temp = opponent_player.take_hit(coor)
                        break
                    except (AlreadyFiredError, InvalidCoordinatesError) as e:
                        print(e)#not necessary, handles random choosing same coor
                else: 
                    print(f'================\nTURN {turn_count}\n================')
                    print('[0] CHECK YOUR BOARD\n[1] CHECK OPPONENTS BOARD\n[2] FIRE\n[3] FIRE SPECIAL SHOT\n================')
                    try:
                        player_input: int = int(input('What would you like to do?: '))

                        if not 0 <= player_input <= 3:
                            # If the input is not between 0 and 3, raise a ValueError
                            raise ValueError

                    except ValueError:
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
                                print('Hit!' if opponent_player.take_hit(coord) else 'Miss!')
                                # Display the opponent's board after the shot
                                opponent_player.display_board_public()
                                input('Press ENTER to continue')
                                break
                                    
                            except (AlreadyFiredError, InvalidCoordinatesError) as e:
                                print(e)
                        case 3:
                            try:
                                # Get the coordinate to fire at
                                opponent_player.display_board_public()
                                coord_input = input(f'Enter a coordinate to fire a special shot (e.g., A1 or A,1): ').replace(' ', '').upper()
                                # Convert the input to a tuple of ints (row, col)
                                coord: tuple[int, int] = Game._parse_coordinate(coord_input)
                                
                                # Check if the shot hit a ship
                                print('Hit!' if opponent_player.take_special_hit(coord) else 'Miss!')
                                # Display the opponent's board after the shot
                                opponent_player.display_board_public()
                                input('Press ENTER to continue')
                                break
                                    
                            except (AlreadyFiredError, InvalidCoordinatesError) as e:
                                print(e)


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
