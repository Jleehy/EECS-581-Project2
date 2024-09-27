"""
This file serves as the main game entrypoint.
It takes the number of ships to play the game with from the
user, validates input, and the starts the gameplay loop.
"""
import sys
from game import Game

def main():

    #print(sys.argv[1])
    while True:
        try:
            #If something that cant be interpreated as an int is input, a ValueError will be raised.
            num_ships: int = int(input('How many ships? (1-5): '))

        except ValueError:
            print('Please input a number.')

            #reprompt the user.
            continue
        
        #reprompt the user if an invalid int is input.
        if not 1 <= num_ships  <= 5:
            print('Please input a number between 1 and 5.')
            continue

        break

    Game(num_ships).loop()

if __name__ == '__main__':
    try:
        main()
    
    #catch SIGINT and print goodbye message. Extra newline for formatting on some terminals.
    except KeyboardInterrupt:
        print("\nGoodbye!")
