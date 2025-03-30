""" enthält die Klasse für einen Raum """

from __future__ import annotations
from .customErrors import RoomsHaveOverlappingPositionError, RoomsNotNearbyError

class Room():
    """ Raum-Klasse mit diverser Logik für Räume """
    def __init__(self, x: int, y: int, isDangerous:bool =False) -> None:
        self.isDangerous = isDangerous
        self.isMarked = False
        self.connections = 0b00000000       # Alle Verbindungen auf 0 initialisieren
        self.x = x
        self.y = y
        self.dangerousNearbyRooms = 0
        self.isRevealed = False
        
        # Sowohl x als auch y müssen ganzzahlige Werte sein
        if not (isinstance(x, int) and isinstance(y, int)):
            raise ValueError("X and Y must be integers for map tile position")
    
    # sind zwei Zellen nebeneinander?
    def roomsNearby(self, other: Room) -> bool:
        if abs(self.x - other.x) <= 1:
            if abs(self.y - other.y) <= 1:
                return True
        
        return False
    
    # ist das Bit in den Connections gesetzt?
    def connectedTo(self, other: Room) -> bool:
        if not self.roomsNearby(other):
            return False
        bitConnection = getBit(self, other)
        return ((1 << bitConnection) & self.connections) > 0
    
    # verbindet zwei Zellen miteinander (dh. schreibt die Connection-Bits um)
    def connectRooms(self, other: Room) -> bool:
        if self.roomsNearby(other):
            
            # Zellen jetzt verbinden
            bitConnectionToOther = getBit(self, other)
            self.connections = self.connections | 1 << bitConnectionToOther
            
            bitConnectionFromOther = getBit(other, self)
            other.connections = other.connections | 1 << bitConnectionFromOther
            
            return True
        return False    
    
    def disconnectRooms(self, other: Room) -> bool:
        if self.roomsNearby(other):
            
            # Zellen jetzt nicht mehr verbinden (logisches XOR => nur das Bit was wir entfernen wollen, wird 0)
            bitConnectionToOther = getBit(self, other)
            self.connections = self.connections ^ 1 << bitConnectionToOther
            
            bitConnectionFromOther = getBit(other, self)
            other.connections = other.connections ^ 1 << bitConnectionFromOther
            
            return True
        return False
    
    # gibt True zurück, wenn der Raum in alle Richtungen umgeben ist
    def allConnectionsOccupied(self) -> bool:
        return self.connections == 0b11111111

    def getNumberOfConnections(self) -> int:
        connections = 0
        for i in range(8):
            if (1<<i) & self.connections > 0:
                connections+=1
        
        return connections
        

# Berechnet im Bezug auf one das Bit das gesetzt sein muss, damit die beiden verbunden sind
def getBit(one: Room, two: Room) -> int:
    xDiff = two.x - one.x
    yDiff = two.y - one.y
    
    match(xDiff):
        case 0:
            match(yDiff):
                case 0:
                    raise RoomsHaveOverlappingPositionError
                case 1:
                    return 4
                case -1:
                    return 0
        case 1:
            match(yDiff):
                case 0:
                    return 2
                case 1:
                    return 3
                case -1:
                    return 1
        case -1:
            match(yDiff):
                case 0:
                    return 6
                case 1:
                    return 5
                case -1:
                    return 7
            
    raise RoomsNotNearbyError
