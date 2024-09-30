

# Battleship - EECS 581 Project 1

## Authors
- **Steve Gan** - [GitHub](https://github.com/qgan99) 
- **Sean Hammell** - [GitHub](https://github.com/seanhammell)
-  **Jacob Leehy** - [GitHub](https://github.com/Jleehy) 
- **Mario Simental** - [GitHub](https://github.com/aepii) 
- **Matthew Sullivan** - [GitHub](https://github.com/matthewsullivan1)

## Overview
This project is a terminal-based **Battleship Game**. We decided to utilize the **Facade Design Pattern** to create our program's overall structure. This pattern allowed for modularization- simplifying the interaction between the main driver, the application (high-level interface), the game boards (game logic), and the ships.

## Design Pattern
The **Facade Design Pattern** allows for a complex system to be simplified by having an interface hide the internal complexities. The `App` class acts as the facade, taking care of the complexities- allowing for communication between `main.py` (the driver), `board.py` (the player's board), `ship.py` (ship object), and `cursor.py` (handles terminal clearing).

## Code Structure

### Terminology
There are several uses of terminology within the code:

`Literal`: Refers to the coordinates of the board- with the following format: 
- **X-Coordinate:** A-J
- **Y-Coordinate:** 1-10
- **Format:** XY

`Index/Indices`: Refers to the coordinates an array uses. 
- `literals_to_indices`, a helper function in the `App` class,  translates the literals to indices.
-  **Column:** 0-9
- **Row:** 0-9
-  **NOTE:** An array is accessed as:  
```
Array[row][column]
```

`Matrix`: Refers to the data structure the `Board` class uses:
- The matrix is a `10x10` array, which supports integers ranging from `0-7`:
	- `0` indicates a blank space.
	- `1-5` indicates spaces that ships cover. Each number belongs to a different-sized ship.
	- `6` indicates a ship that has been hit.
	- `7` indicates an attempted shot which leads to a miss.

### `main.py` - Game Driver
This is the starting point for the game. It is responsible for the primary gameplay loop.
1. **I/O:** Gets player names, number of ships to be played, prompts for ship placements, and ship attacks.
2. **Initialization:** Initializes an `App` object and two players with `Board` objects.
3. **Gameplay Loop:** Manages turns between players, allowing them to place ships and attack each other's boards.
4. **Game Logic:** Makes calls to `App` to handle ship placement, ship attacks and board rendering.

### `app.py` - The Facade
The `App` class provides a simplified interface for interacting with the players' `Board` objects and managing the flow of the game. The `App` class stores two `Board` objects (one for each player) the number of ships to be played, and a [config](#boardpy---players-board).

**Design Structure:** Calls are made to `App` from `main.py`, which then forwards calls to `Board`. In other words, `App` handles input and parsing, while `Board` handles validity and game logic.

**NOTE:** `Literals` are passed to `App`.

- `place_ship`: Parses input to place a ship on a player's `Board` given literal position and ship size.
- `attack`: Parses input to manage attacks made by the player. Communicates to the attacker's and defender's `Board` objects, calling `attack` and `defend` respectively.
- `print_board`: Prints a player's board. 
- `literals_to_indices`: Converts `literal` coordinates to `indices`.
- `check_quit`: Checks if Q is entered into prompts, which exits the program.
- `prompt_ship_coordinate`: Prompts user for a ship coordinate (`literal`). 
- `prompt_ship_coordinate`: Prompts user for an attack coordinate (`literal`).
- `prompt_num_ships`: Prompts the user for the number of ships to be played with.
- `_is_valid_coordinate`: Helper function to determine if a given coordinate (`literal`) is valid.

### `board.py` - Player's Board
The `Board` class handles the overall game logic. Each player is assigned a `Board` which contains:
- **Matrix:** The board's data structure, where:
	- The matrix is a `10x10` array, which supports integers ranging from `0-7`:
		- `0` indicates a blank space.
		- `1-5` indicates spaces that ships cover. Each number belongs to a different-sized ship.
		- `6` indicates a ship that has been hit.
		- `7` indicates an attempted shot which leads to a miss.
	- Each integer also has a color assigned to it, which the board renders. Colors can be changed via the **config** stored in the `App` class.
- **Ships:** Stores `Ship` objects in an array.
- **Shots:** Stores attempted shot coordinates (`literals`) in a set.

**NOTE:** `Indices` are passed to `Board`.

- `place_ship`: Places a ship on a player's `Board` given indices and ship size. Handles validity and logic.
- `attack`: Manages attacks made by the player. Handles validity and logic.
- `defend`: Manages attacks made to the player. Handles validity and logic.
- `is_overlapping`: Determine if ships overlap.
- `is_correct_length`: Determines if a ship being placed matches the correct length specified by the prompt.
- `is_diagonal`: Checks if a ship placement attempt is diagonal.
- `_update_matrix`: Updates the `Board` matrix given row, column, and a value.
- `all_ships_sunk`: Determines if all ships are sunk.

### `ship.py` - Ship Logic
The `Ship` class handles the logic of the ships used in a `Board`. It manages the placement, overlap conditions, and sinking of the ship. Each ship contains:
- **Indices:** A set containing tuples of `incidices`, which represents `indices` on the `matrix` the ship covers.

- `_populate_indices`: Add the indices a ship covers to the set.
- `is_overlapping`: Checks if the ship overlaps with another ship.


### `cursor.py` - Cursor Logic
Handles terminal positioning and clearing.

- `move_to`:  Moves the cursor to the beginning of line n.
- `move_up`: Moves the cursor to the beginning of the previous line, n lines up.
- `erase`: Erases everything from the cursor to the end of the screen.

## Game Loop
1.  **Game Initialization:**
-   `main.py` initializes two players with their boards.
-   The App prompts each player to place their ships using the place_ship method.
2.  **Placing Ships:**
-   The `App` parses the player's input into board coordinates and passes the information to the `Board` for validation and placement.
3.  **Attacking:**
-   During each turn, `main.py` prompts the current player to attack using the `App`.
-   The `App` checks if the attack hits a ship, updates the board, and returns the results.
4.  **Winning:**
The game continues until one player has successfully sunk all ships, and the `App` declares the winner.



