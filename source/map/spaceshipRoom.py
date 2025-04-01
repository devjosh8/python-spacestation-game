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
        """ testet, ob Räume nebeneinander sind. Gibt TRUE oder FALSE zurück """
        if abs(self.x - other.x) <= 1:
            if abs(self.y - other.y) <= 1:
                return True
        
        return False
    
    # ist das Bit in den Connections gesetzt?
    def connectedTo(self, other: Room) -> bool:
        """ testet, ob Räume verbunden sind. Gibt TRUE oder FALSE zurück """
        if not self.roomsNearby(other):
            return False
        bitConnection = getBitByOffset(self, other)
        return ((1 << bitConnection) & self.connections) > 0
    
    # verbindet zwei Räume miteinander (dh. schreibt die Connection-Bits um)
    def connectRooms(self, other: Room) -> bool:
        """ Verbindet zwei Räume. Gibt TRUE zurück, wenn die Verbindung erfolgreich war
            testet NICHT, ob eine Verbindung schon bestand """
        if self.roomsNearby(other):
            
            # Räume jetzt verbinden
            bitConnectionToOther = getBitByOffset(self, other)
            self.connections = self.connections | 1 << bitConnectionToOther
            
            bitConnectionFromOther = getBitByOffset(other, self)
            other.connections = other.connections | 1 << bitConnectionFromOther
            
            return True
        return False    
    
    def disconnectRooms(self, other: Room) -> bool:
        """ Entfernt die Verbindung von zwei Räumen. Gibt TRUE zurück, wenn die Räume nebeneinander sind  
            und keine Verbindung hatten, oder wenn die Verbindung entfernt wurde"""
        if self.roomsNearby(other):
            
            # Zellen jetzt nicht mehr verbinden (logisches XOR => nur das Bit was wir entfernen wollen, wird 0)
            bitConnectionToOther = getBitByOffset(self, other)
            self.connections = self.connections ^ 1 << bitConnectionToOther
            
            bitConnectionFromOther = getBitByOffset(other, self)
            other.connections = other.connections ^ 1 << bitConnectionFromOther
            
            return True
        return False
    
    # gibt True zurück, wenn der Raum in alle Richtungen umgeben ist
    def allConnectionsOccupied(self) -> bool:
        """ gibt zurück, ob ein Raum in alle Richtungen verbunden ist """
        return self.connections == 0b11111111

    def getNumberOfConnections(self) -> int:
        """ Gibt die Anzahl der Verbindungen eines Raumes zu anderen Räumen zurück """
        connections = 0
        for i in range(8):
            if (1<<i) & self.connections > 0:
                connections+=1
        
        return connections
        
# Berechnet im Bezug auf one das Bit das gesetzt sein muss, damit die beiden verbunden sind
def getBitByOffset(one: Room, two: Room) -> int:
    """ Berechnet das Bit, das gesetzt sein muss, damit one mit two verbunden ist """
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
