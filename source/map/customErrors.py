""" Custom Errors für Fehlerbehandlung bei Rooms"""

class RoomsNotNearbyError(Exception):
    
    def __init__(self) -> None:
        super().__init__("Tiles are not nearby!")

class RoomsHaveOverlappingPositionError(Exception):
    
    def __init__(self) -> None:
        super().__init__("Tiles have the same position!")
