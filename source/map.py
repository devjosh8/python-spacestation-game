from __future__ import annotations
from . custom_errors import *

#       Verbindungen
#
#         7   0   1
#          \  |  /
#           #####
#      6 -  #   # - 2
#           #####
#          /  |  \
#         5   4   3
#
# Verbindungen werden als 8 Bit (1 Byte) pro Zelle gespeichert. Dabei gibt
# zum Beispiel Bit 8, wenn es 1 ist, die Verbindung zur Zelle oben links an

class MapTile():
    
    def __init__(self, x, y, isDangerous):
        self.isDangerous = isDangerous
        self.connections = 0 << 8       # Alle Verbindungen auf 0 initialisieren
        self.x = x
        self.y = y
        
        # Sowohl x als auch y müssen ganzzahlige Werte sein
        if not (isinstance(x, int) and isinstance(y, int)):
            raise ValueError("X and Y must be integers for map tile position")
    
    # sind zwei Zellen nebeneinander?
    def tilesNearby(self, other: MapTile):
        if abs(self.x - other.x) <= 1:
            if abs(self.y - other.y) <= 1:
                return True
        
        return False
    
    # ist das Bit in den Connections gesetzt?
    def connectedTo(self, other: MapTile):
        if not self.tilesNearby(other):
            return False
        bitConnection = getBit(self, other);
        return ((1 << bitConnection) & self.connections) > 0
    
    # verbindet zwei Zellen miteinander (dh. schreibt die Connection-Bits um)
    def connectTiles(self, other: MapTile):
        # Zellen dürfen sich um maximal 1 bei beiden Koordinaten unterscheiden
        if self.tilesNearby(other):
            
            # Zellen jetzt verbinden
            bitConnectionToOther = getBit(self, other)
            self.connections = self.connections | 1 << bitConnectionToOther
            
            bitConnectionFromOther = getBit(other, self)
            other.connections = other.connections | 1 << bitConnectionFromOther
            
            return True
        
        return False    
            

    
class Map():
    
    def __init__(self, size):
        self.size = size
        self.tiles = [size][size] # Speichert die ganzen Tiles, die die Map ausmachen
    
    def generate_map():
        pass
    

# Berechnet im Bezug auf one! das Bit das gesetzt sein muss, damit die beiden verbunden sind
def getBit(one: MapTile, two: MapTile):
    xDiff = two.x - one.x
    yDiff = two.y - one.y
    
    match(xDiff):
        case 0:
            match(yDiff):
                case 0:
                    raise TilesCorrespondError
                case 1:
                    return 0
                case -1:
                    return 4
        case 1:
            match(yDiff):
                case 0:
                    return 2
                case 1:
                    return 1
                case -1:
                    return 3
        case -1:
            match(yDiff):
                case 0:
                    return 6
                case 1:
                    return 7
                case -1:
                    return 5
            
    raise TilesNotNearbyError