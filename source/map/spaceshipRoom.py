from __future__ import annotations
from .customErrors import *

class Room():
    
    def __init__(self, x, y, isDangerous=False):
        self.isDangerous = isDangerous
        self.connections = 0b00000000       # Alle Verbindungen auf 0 initialisieren
        self.x = x
        self.y = y
        
        # Sowohl x als auch y müssen ganzzahlige Werte sein
        if not (isinstance(x, int) and isinstance(y, int)):
            raise ValueError("X and Y must be integers for map tile position")
    
    # sind zwei Zellen nebeneinander?
    def tilesNearby(self, other: Room):
        if abs(self.x - other.x) <= 1:
            if abs(self.y - other.y) <= 1:
                return True
        
        return False
    
    # ist das Bit in den Connections gesetzt?
    def connectedTo(self, other: Room):
        if not self.tilesNearby(other):
            return False
        bitConnection = getBit(self, other);
        return ((1 << bitConnection) & self.connections) > 0
    
    # verbindet zwei Zellen miteinander (dh. schreibt die Connection-Bits um)
    def connectTiles(self, other: Room):
        # Zellen dürfen sich um maximal 1 bei beiden Koordinaten unterscheiden
        if self.tilesNearby(other):
            
            # Zellen jetzt verbinden
            bitConnectionToOther = getBit(self, other)
            self.connections = self.connections | 1 << bitConnectionToOther
            
            bitConnectionFromOther = getBit(other, self)
            other.connections = other.connections | 1 << bitConnectionFromOther
            
            return True
        return False    
    
    # gibt True zurück, wenn der Raum in alle Richtungen umgeben ist
    def allConnectionsOccupied(self):
        return (self.connections == 0b11111111)




# Berechnet im Bezug auf one das Bit das gesetzt sein muss, damit die beiden verbunden sind
def getBit(one: Room, two: Room):
    xDiff = two.x - one.x
    yDiff = two.y - one.y
    
    match(xDiff):
        case 0:
            match(yDiff):
                case 0:
                    raise TilesCorrespondError
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
            
    raise TilesNotNearbyError
