

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
We implemented the ai player by creating an ai class which is a subclass of the player class. This allows us to retain the original functionality of the game and take advantage of the prestablished code base. From here, we implemented the three difficulty modes and a handful of helper functions to aid us in integrating the player class. In addition, the game class needed to be adjusted in order to account for the possibility of an ai player. In order to do this, we created a _build_ai_player function which closely mirrors the previous _build_player function in order to handle the logic associated with having an ai player. Fianlly, the main game loop was adjusted in order to integrate the ai player into the gameflow of the main game.


### Special Shot





