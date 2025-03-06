from __future__ import annotations
from .spaceshipRoom import *
from .mapHelper import *
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
                possibleDirections = [i for i in range(8) if (selectedTile.connections & (1 << i)) == 0]
                randomDirection = random.choice(possibleDirections)
                xOffset, yOffset = getPositionOffsetByDirection(randomDirection)
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

        # zufällig gefährliche Räume generieren
        room: Room
        for room in self.getMapTiles():
            if random.randint(0, 3) == 0:
                room.isDangerous = True

        # der Startraum ist in jedem Fall nicht gefährlich
        self.getStartingTile().isDangerous = False

        # Für jeden Raum die Anzahl an gefährlichen Nachbarräumen setzen
        for room in self.getMapTiles():
            connectedRooms: Room
            dangerousNearbyRooms = 0
            for connectedRooms in self.getNeighbouringTilesWithConnection(room):
                if connectedRooms.isDangerous:
                    dangerousNearbyRooms+=1
            room.dangerousNearbyRooms = dangerousNearbyRooms
            # Nur Räume, die nicht gefährlich sind, können schon gescannt sein!
            if not room.isDangerous and random.randint(0, 1) == 0:
                room.isRevealed = True
            
    def addMapTile(self, tile: Room):
        self.tiles.append(tile)
        
    def getMapTiles(self):
        return self.tiles
    
    
    def print(self, colors=None, defaultColor=None, safeColor=None):
        # Ein 2D Array erstellen mit den Dimensionen size * size initialisiert auf alles ' ' 
        # Wichtig!!! Im Buffer kommt zuerst die Y-Koordinate, dann die X Koordinate!
        buffer = [["." for i in range(self.size * 2 + 1)] for j in range(self.size * 2 + 1)]
        
        # Durchlauf, um Räume und Farben zu platzieren
        tile: Room
        for tile in self.tiles:
            
            roomChar = "#"
            if tile.isRevealed:
                roomChar = (safeColor + str(tile.dangerousNearbyRooms) + defaultColor)
            
            if colors != None and (tile.x, tile.y) in colors:
                tileColor = colors[(tile.x, tile.y)]
                buffer[tile.y*2+1][tile.x*2+1] = (tileColor + roomChar + defaultColor)
            else:
                buffer[tile.y*2+1][tile.x*2+1] = roomChar
        
        # erster Durchlauf um die Wege zu platzieren
        for tile in self.getMapTiles():
            for neighbor in self.getNeighbouringTilesWithConnection(tile):
                posOffsetX = neighbor.x - tile.x
                posOffsetY = neighbor.y - tile.y
                
                directionIndex = getDirectionIndexByPositionOffset( (posOffsetX, posOffsetY) )
                char = getTextCharacterByDirection(directionIndex)
                
                buffer[tile.y*2 + posOffsetY + 1][tile.x*2 + posOffsetX + 1] = char 
                
        # zweiter Durchlauf, um Diagonalverbindungen richtig zu platzieren 
        # vorheriger Code hat ergeben, dass beide Schleifen NICHT in eine gepackt werden können
        # und seperat gehalten werden müssen!! TODO: Code optimieren
        for tile in self.getMapTiles():
            for neighbor in self.getNeighbouringTilesWithConnection(tile):
                posOffsetX = neighbor.x - tile.x
                posOffsetY = neighbor.y - tile.y
                
                directionIndex = getDirectionIndexByPositionOffset( (posOffsetX, posOffsetY) )
                char = getTextCharacterByDirection(directionIndex)
                if char == "/" and buffer[tile.y*2+posOffsetY + 1][tile.x*2+posOffsetX + 1] == "\\":
                    char = "X"
                    buffer[tile.y*2 + posOffsetY + 1][tile.x*2 + posOffsetX + 1] = char 
                if char == "\\" and buffer[tile.y*2+posOffsetY + 1][tile.x*2+posOffsetX + 1] == "/":
                    char = "X"
                    buffer[tile.y*2 + posOffsetY + 1][tile.x*2 + posOffsetX + 1] = char 
        
        # schließlich den Buffer printen (mit Grid, um auszuwählen)
        print("\t", end="")
        for x in range(self.size):
            print(" " + str(x), end="")
        print()
        for x in range(self.size*2+1):
            if x % 2 != 0:
                print(str(int((x-1)/2)) + "\t", end="")
            else:
                print("\t", end="")
            for y in range(self.size*2+1):
                print(buffer[x][y], end="")
            print("")

    def getTileAt(self, x, y):
        room: Room
        for room in self.getMapTiles():
            if room.x == x and room.y == y:
                return room
        
        raise ValueError("No such room")
    
    def tileExists(self, x, y):
        room: Room
        for room in self.getMapTiles():
            if room.x == x and room.y == y:
                return True
        return False
    
    def getStartingTile(self):
        genX = int(self.size / 2)
        genY = int(self.size / 2)
        return self.getTileAt(genX, genY)

    # gibt alle Nachbar-Räume eines Raums zurück im Koordinatenformat (x,y), die mit dem Raum "tile" Verbunden sind
    def getNeighbouringTilesWithConnection(self, tile: Room):
        neighbours = []
        
        for i in range(8):
            shift = (1 << i) & 0b11111111
            if shift & tile.connections != 0:
                xOffset, yOffset = getPositionOffsetByDirection(i)
                
                neighbours.append(self.getTileAt(tile.x + xOffset, tile.y + yOffset))
                
        return neighbours
    
    def getNeighbouringTilesWithoutConnection(self, tile: Room):
        neighbours = []
        
        for i in range(8):
            xOffset, yOffset = getPositionOffsetByDirection(i)
            if self.tileExists(xOffset, yOffset):
                neighbours.append(self.getTileAt(tile.x + xOffset, tile.y + yOffset))
                
        return neighbours