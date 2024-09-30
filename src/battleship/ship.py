"""
Name of program: ship.py
Description: Class to hold information on ships.
Inputs: None
Outputs: None
Other sources for code: N/A
<<<<<<< Updated upstream
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le, Steve Gan, Sean Hammell, Jacob Leehy, Mario Simental, Matthew Sullivan
=======
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le
Authors: Steve Gan, Sean Hammell, Jacob Leehy, Mario Simental, Matthew Sullivan
>>>>>>> Stashed changes
Creation date: 09/11/24
"""

from exceptions import InvalidShipLengthError, InvalidCoordinatesError #import exceptions.

class Ship: # ship class
    """
    Represents a particular ship on the board, as well as the health of said ship.
    """

    def __init__(self, ship_length: int, start_coord: tuple[int, int], end_coord: tuple[int, int]) -> None: # constructor
        """
        Constructor for ship class.
        """
        
        #make sure shio length is valid.
        if not (0 < ship_length < 11): # if not a valid length
            # Raise an exception if the ship length is invalid
            raise InvalidShipLengthError('Invalid ship length! Must be between 1 and 10.') # raise an invalid ship length error

        self._ship_length: int = ship_length #stores param value

        if not (0,0) <= start_coord <= (9,9): # if not valid
            # Raise an exception if the start coordinate is invalid
            raise InvalidCoordinatesError('Invalid start coordinate! Must be between (0,0) and (9,9).') #invalid coordinate

        if not (0,0) <= end_coord <= (9,9): # if not valid
            # Raise an exception if the end coordinate is invalid
            raise InvalidCoordinatesError('Invalid end coordinate! Must be between (0,0) and (9,9).') # invalid coordinate
        
        if start_coord > end_coord: # swap coords if needed - lul, we used the same janky solution
            temp: tuple[int, int] = end_coord # Swap the coordinates if the start coordinate is greater than the end coordinate
            end_coord: tuple[int, int] = start_coord # Swap the coordinates
            start_coord: tuple[int, int] = temp # Swap the coordinates

        if end_coord[0] - start_coord[0] == self._ship_length and end_coord[1] - start_coord[1] == self._ship_length: # if bad length
            # Raise an exception if the ship length does not match the distance between the coordinates
            raise InvalidCoordinatesError('Tried to place ship in coordinates that don\'t match length.') # raise error
        
        if start_coord[0] == end_coord[0]: #implies horizontal placement.
            if abs(start_coord[1] - end_coord[1]) + 1 != ship_length: # Raise an exception if the ship length does not match the distance between the coordinates
                raise InvalidCoordinatesError('Ship length does not match distance between coordinates') # raise error
            self._ship_length: int = ship_length # Set the ship length
            self._hull: list[tuple[int, int, bool]] = [(start_coord[0], y, False) for y in range(start_coord[1], end_coord[1]+1)] # Set the hull

        elif start_coord[1] == end_coord[1]: #implies vertical placement.
            if abs(start_coord[0] - end_coord[0]) + 1!= ship_length: # Raise an exception if the ship length does not match the distance between the coordinates
                raise InvalidCoordinatesError('Ship length does not match distance between coordinates') # Raise an exception if the ship length does not match the distance between the coordinates
            self._ship_length: int = ship_length #set ship length
            self._hull: list[tuple[int, int, bool]] = [(x, start_coord[1], False) for x in range(start_coord[0], end_coord[0]+1)] # Set the hull

        else: # else
            raise InvalidCoordinatesError('Invalid ship placement! Make sure that it is horizontal or vertical.') # raise error

    
    @property #property
    def sunk(self) -> bool: #def sunk
        return all(map(lambda x: x[2], self._hull)) #Returns True if the ship is sunk, False otherwise.

    @property #property
    def ship_length(self) -> int: #def length
        return self._ship_length #Length of ship as an immutable attribute.

    @property #property
    def hull(self) -> list[tuple[int, int, bool]]: #def hull
        return self._hull #Returns the hull of the ship.

    def take_hit(self, hit: tuple[int, int]) -> None: #def take hit
        """Mark the hit on the ship."""
        for idx, (x,y,_) in enumerate(self._hull): #iterate over hulls
            # If the hit is on the ship
            if hit == (x,y): # if coord hit
                # Mark the hit on the ship
                self._hull[idx] = (hit) + (True, ) # mark hit
                return # return
        raise ValueError('Invalid coordinates, no vulnerable ship hull at this location.') #raise error
