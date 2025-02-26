from __future__ import annotations
from .spaceshipRoom import *
import random

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

    
class Map():
    
    def __init__(self, size):
        self.size = size
        self.tiles = [] # Speichert die ganzen Tiles, die die Map ausmachen
    
    # Die Karte generieren
    def generateMap(self):
        generatedRooms = 0
        
        while(generatedRooms < 35):
            # in der Mitte der Karte anfangen
            if generatedRooms == 0:
                genX = int(self.size / 2)
                genY = int(self.size / 2)
                
                newTile = Room(genX, genY, False)
                self.addMapTile(newTile)
                
            else:
                # zufälligen Raum auswählen
                selectedTile:Room = random.choice(self.getMapTiles())
                # weitermachen, wenn alle Richtungen blockiert sind
                if selectedTile.allConnectionsOccupied():
                    continue
                
                # eine zufällige Richtung auswählen -> alle möglichen Richtungen sind 0 in der Bitmaske
                # alle Bits durchgehen und alle die 0 sind in eine Liste hinzufügen
                possibleDirections = [i for i in range(8) if (selectedTile.connections & 1 << i) == 0]
                direction = random.choice(possibleDirections)
                xOffset, yOffset = getPositionOffsetByDirection(direction)
                newX = selectedTile.x + xOffset
                newY = selectedTile.y + yOffset
                
                # neue Koordinaten validieren und gegebenenfalls neu versuchen
                if newX < 0 or newY < 0 or newX >= self.size or newY >= self.size:
                    continue
                
                
                # befindet sich an dieser Stelle bereits ein Tile?
                # wenn ja, beide Tiles verbinden und abbrechen
                tileFound = False
                for lookupTile in self.getMapTiles():
                    if lookupTile.x == newX and lookupTile.y == newY:
                        selectedTile.connectTiles(lookupTile)
                        tileFound = True
                
                if tileFound:
                    continue
                
                # ansonsten neues Tile erstellen und mit dem aktuellen verbinden
                newTile = Room(selectedTile.x + xOffset, selectedTile.y + yOffset)
                newTile.connectTiles(selectedTile)
                self.addMapTile(newTile)
                
            generatedRooms+=1
    
    def addMapTile(self, tile: Room):
        self.tiles.append(tile)
        
    def getMapTiles(self):
        return self.tiles
    
    def print(self):
        # Ein 2D Array erstellen mit den Dimensionen size * size initialisiert auf alles ' ' 
        buffer = [[" " for i in range(self.size)] for j in range(self.size)]
        
        tile: Room
        for tile in self.tiles:
            buffer[tile.x][tile.y] = "#"
        
        for x in range(self.size):
            for y in range(self.size):
                print(buffer[x][y], end="")
            print("")


# gibt die Richtung in eine Verbindung anhand der Nummer der Richtung zurück
def getPositionOffsetByDirection(direction):
    match(direction):
        case 0:
            return (0, 1)
        case 1:
            return (1, 1)
        case 2:
            return (1, 0)
        case 3:
            return (1, -1)
        case 4:
            return (0, -1)
        case 5:
            return (-1, -1)
        case 6:
            return (-1, 0)
        case 7:
            return (-1, 1)
    raise ValueError("Directional number could not be converted into acutal coordinated")