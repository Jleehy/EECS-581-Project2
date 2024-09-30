"""
This file serves as the main game entrypoint.
It takes the number of ships to play the game with from the
user, validates input, and the starts the gameplay loop.
"""
import sys #import for sys
from game import Game # import game

def main(): #def main func

    #print(sys.argv[1])
    while True: # while true
        try: #try
            #If something that cant be interpreated as an int is input, a ValueError will be raised.
            num_ships: int = int(input('How many ships? (1-5): ')) # get num ships

        except ValueError: #raise error if needed
            print('Please input a number.') # ask reinput

            #reprompt the user.
            continue # continue
        
        #reprompt the user if an invalid int is input.
        if not 1 <= num_ships  <= 5: #check valid
            print('Please input a number between 1 and 5.') #tell bad
            continue #continue

        break #break

    Game(num_ships).loop() #call loop

if __name__ == '__main__': #main magic
    try: #try
        main() #call main
    
    #catch SIGINT and print goodbye message. Extra newline for formatting on some terminals.
    except KeyboardInterrupt:
        print("\nGoodbye!")
