"""
Name of program: ship.py
Description: Class to hold information on ships.
Inputs: None
Outputs: None
Other sources for code: N/A
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le
Creation date: 09/11/24
"""

#import exceptions.
from exceptions import InvalidShipLengthError, InvalidCoordinatesError

class Ship:
    """
    Represents a particular ship on the board, as well as the health of said ship.
    """

    def __init__(self, ship_length: int, start_coord: tuple[int, int], end_coord: tuple[int, int]) -> None:
        """
        Constructor for ship class.
        """
        
        #make sure shio length is valid.
        if not (0 < ship_length < 11):
            # Raise an exception if the ship length is invalid
            raise InvalidShipLengthError('Invalid ship length! Must be between 1 and 10.')

        self._ship_length: int = ship_length

        if not (0,0) <= start_coord <= (9,9):
            # Raise an exception if the start coordinate is invalid
            raise InvalidCoordinatesError('Invalid start coordinate! Must be between (0,0) and (9,9).')

        if not (0,0) <= end_coord <= (9,9):
            # Raise an exception if the end coordinate is invalid
            raise InvalidCoordinatesError('Invalid end coordinate! Must be between (0,0) and (9,9).')
        
        if start_coord > end_coord:
            # Swap the coordinates if the start coordinate is greater than the end coordinate
            temp: tuple[int, int] = end_coord
            # Swap the coordinates
            end_coord: tuple[int, int] = start_coord
            # Swap the coordinates
            start_coord: tuple[int, int] = temp

        if end_coord[0] - start_coord[0] == self._ship_length and end_coord[1] - start_coord[1] == self._ship_length:
            # Raise an exception if the ship length does not match the distance between the coordinates
            raise InvalidCoordinatesError('Tried to place ship in coordinates that don\'t match length.')
        
        #implies horizontal placement.
        if start_coord[0] == end_coord[0]:
            # Raise an exception if the ship length does not match the distance between the coordinates
            if abs(start_coord[1] - end_coord[1]) + 1 != ship_length:
                raise InvalidCoordinatesError('Ship length does not match distance between coordinates')
            # Set the ship length
            self._ship_length: int = ship_length
            # Set the hull
            self._hull: list[tuple[int, int, bool]] = [(start_coord[0], y, False) for y in range(start_coord[1], end_coord[1]+1)]

        #implies vertical placement.
        elif start_coord[1] == end_coord[1]:
            # Raise an exception if the ship length does not match the distance between the coordinates
            if abs(start_coord[0] - end_coord[0]) + 1!= ship_length:
                # Raise an exception if the ship length does not match the distance between the coordinates
                raise InvalidCoordinatesError('Ship length does not match distance between coordinates')
            self._ship_length: int = ship_length
            # Set the hull
            self._hull: list[tuple[int, int, bool]] = [(x, start_coord[1], False) for x in range(start_coord[0], end_coord[0]+1)]

        else:
            raise InvalidCoordinatesError('Invalid ship placement! Make sure that it is horizontal or vertical.')

    
    @property
    def sunk(self) -> bool:
        """Returns True if the ship is sunk, False otherwise."""
        return all(map(lambda x: x[2], self._hull))

    @property
    def ship_length(self) -> int:
        """Length of ship as an immutable attribute."""
        return self._ship_length

    @property
    def hull(self) -> list[tuple[int, int, bool]]:
        """Returns the hull of the ship."""
        return self._hull

    def take_hit(self, hit: tuple[int, int]) -> None:
        """Mark the hit on the ship."""
        for idx, (x,y,_) in enumerate(self._hull):
            # If the hit is on the ship
            if hit == (x,y):
                # Mark the hit on the ship
                self._hull[idx] = (hit) + (True, )
                return
        raise ValueError('Invalid coordinates, no vulnerable ship hull at this location.')
