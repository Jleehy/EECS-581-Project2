

# Battleship - EECS 581 Project 2

## Authors
- **Steve Gan** - [GitHub](https://github.com/qgan99) 
- **Sean Hammell** - [GitHub](https://github.com/seanhammell)
-  **Jacob Leehy** - [GitHub](https://github.com/Jleehy) 
- **Mario Simental** - [GitHub](https://github.com/aepii) 
- **Matthew Sullivan** - [GitHub](https://github.com/matthewsullivan1)

## Overview
This project is an extension of project one and includes the addition of ai players and a special shot feature. It retains the structure of the previous teams code, so their documentation and readme is still applicable.

## Added Features

### Ai Player
The ai player was designed to follow the patter lain out by the assignment instructions, with there being three difficulties described as follows:

i. Easy: It just fires randomly every turn.
ii. Medium: It fires randomly until it hits a ship then fires in orthogonally adjacent
spaces to find other hits until a ship is sunk.
iii. Hard: Cheater, cheater pumpkin eater! This mode knows where all your ships
are and lands a hit every turn.

We implemented the ai player by creating an ai class which is a subclass of the player class. This allowed us to retain the original functionality of the game and take advantage of the prestablished code base. From here, we implemented the three difficulty modes and a handful of helper functions to aid us in integrating the player class. In addition, the game class needed to be adjusted in order to account for the possibility of an ai player. In order to do this, we created a _build_ai_player function which closely mirrors the previous _build_player function in order to handle the logic associated with having an ai player. Fianlly, the main game loop was adjusted in order to integrate the ai player into the gameflow of the main game.


### Special Shot
Our bonus feature we decided to implement was a 3x3 special shot which does an area of affect attack on the opponents board. At the beginning of the game, players can choose the number of special shots they want to play with. In order to implement special shots, we needed to adjust both the player class and the game class. In the player class, we implemented the majority of the logic for how the shot would be handled. This predominantly focused on board updates to account for the 3x3 radius of the shot. In the game class, we integrated the user input needed to handle the special shots. This included updating both the __init__ function and the main game loop.




