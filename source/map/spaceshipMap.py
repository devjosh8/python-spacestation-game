""" enthält die Map-Klasse, die eine Karte für das Spiel ist """

from __future__ import annotations
import random
from .spaceshipRoom import Room
from .mapHelper import getDirectionByPositionOffset, getPositionOffsetByDirection, getTextCharacterByDirection

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
    """ Map, Einheit für die Karte, enthält Räume und Logikfunktionen """
    def __init__(self, size: int, dangerousRoomsPropability:float =1/3) -> None:
        self.size = size
        self.tiles: list[Room] = [] # Speichert die ganzen Tiles, die die Map ausmachen
        self.dangerousRoomsPropability = dangerousRoomsPropability
    
    # Die Karte generieren
    def generateMap(self) -> None:
        generatedRooms = 0
        
        while generatedRooms < 50:
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
                        selectedTile.connectRooms(lookupTile)
                        tileFound = True
                
                if tileFound:
                    continue
                
                # ansonsten neues Tile erstellen und mit dem aktuellen verbinden
                newTile = Room(selectedTile.x + xOffset, selectedTile.y + yOffset)
                newTile.connectRooms(selectedTile)
                self.addMapTile(newTile)
                
            generatedRooms+=1
            
        self._removeRoomsWithSingleConnection()
        self._generateDangerousRooms()

    def _removeRoomsWithSingleConnection(self) -> None:
        roomWithSingleConnectionExist = True
        roomsToRemoveNextIteration: list[Room] = []
        while roomWithSingleConnectionExist:
            roomToRemove: Room
            for roomToRemove in roomsToRemoveNextIteration:
                neighbours = self.getNeighbouringTilesWithConnection(roomToRemove)
                # Prämisse => roomToRemove hat nur einen Nachbar
                
                if len(neighbours) != 1:
                    raise ValueError("Map generation error: Room which is supposed to have only 1 neighbour has 0 or more than 1")
                
                for neighbouringRoom in neighbours:
                    roomToRemove.disconnectRooms(neighbouringRoom)
                
                self.removeMapTile(roomToRemove)
            
            roomsToRemoveNextIteration.clear()
            
            roomWithSingleConnectionExist = False
            for room in self.getMapTiles():
                if room.getNumberOfConnections() == 1:
                    roomsToRemoveNextIteration.append(room)
                    roomWithSingleConnectionExist = True 

        
    def _generateDangerousRooms(self) -> None:
        # zufällig gefährliche Räume generieren
        room: Room
        for room in self.getMapTiles():
            if random.randint(0, int(1/self.dangerousRoomsPropability)) == 0:
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
            
    def addMapTile(self, tile: Room) -> None:
        self.tiles.append(tile)
        
    def removeMapTile(self, tile: Room) -> None:
        self.tiles.remove(tile)
        
    def getMapTiles(self) -> list[Room]:
        return self.tiles
    
    
    def _createPrintBuffer(self, defaultColor:str ="", safeColor:str ="", markColor:str ="") -> list[list[str]]:
        # Ein 2D Array erstellen mit den Dimensionen size * size initialisiert auf alles ' ' 
        # Wichtig!!! Im Buffer kommt zuerst die Y-Koordinate, dann die X Koordinate!
        # Einen Punkt . jeweils nur in jede zweite Spalte und Zeile platzieren, damit das Raster nicht voll mit Punkten ist
        # und für den User die Zusammenhänge zwischen Zeile und Spalte besser ersichtlich machen, statt einem Punkte spam
        buffer = [[("." if i % 2 != 0 and j % 2 != 0 else " ") for i in range(self.size * 2 + 1)] for j in range(self.size * 2 + 1)]

        # Durchlauf, um Räume und Farben zu platzieren
        tile: Room
        for tile in self.tiles:
            
            roomChar = "#"
            if tile.isRevealed:
                roomChar = safeColor + str(tile.dangerousNearbyRooms) + defaultColor
            
            elif tile.isMarked:
                roomChar = markColor + "#" + defaultColor
            
            buffer[tile.y*2+1][tile.x*2+1] = roomChar
        
        # erster Durchlauf um die Wege zu platzieren
        for tile in self.getMapTiles():
            for neighbor in self.getNeighbouringTilesWithConnection(tile):
                posOffsetX = neighbor.x - tile.x
                posOffsetY = neighbor.y - tile.y
                
                directionIndex = getDirectionByPositionOffset( (posOffsetX, posOffsetY) )
                char = getTextCharacterByDirection(directionIndex)
                
                buffer[tile.y*2 + posOffsetY + 1][tile.x*2 + posOffsetX + 1] = char 
                
        # zweiter Durchlauf, um Diagonalverbindungen richtig zu platzieren 
        # vorheriger Code hat ergeben, dass beide Schleifen NICHT in eine gepackt werden können
        # und seperat gehalten werden müssen!!
        for tile in self.getMapTiles():
            for neighbor in self.getNeighbouringTilesWithConnection(tile):
                posOffsetX = neighbor.x - tile.x
                posOffsetY = neighbor.y - tile.y
                
                directionIndex = getDirectionByPositionOffset( (posOffsetX, posOffsetY) )
                char = getTextCharacterByDirection(directionIndex)
                if char == "/" and buffer[tile.y*2+posOffsetY + 1][tile.x*2+posOffsetX + 1] == "\\":
                    char = "X"
                    buffer[tile.y*2 + posOffsetY + 1][tile.x*2 + posOffsetX + 1] = char 
                if char == "\\" and buffer[tile.y*2+posOffsetY + 1][tile.x*2+posOffsetX + 1] == "/":
                    char = "X"
                    buffer[tile.y*2 + posOffsetY + 1][tile.x*2 + posOffsetX + 1] = char 
        return buffer
        
    def print(self, defaultColor:str ="", safeColor:str ="", markColor:str ="") -> None:
        buffer = self._createPrintBuffer(defaultColor=defaultColor, safeColor=safeColor, markColor=markColor)
        # Spaltenanzeige printen
        print("\t", end="")
        for x in range(self.size):
            print(" " + str(x), end="")
            
        print()
            
        for x in range(self.size*2+1):
            if x % 2 != 0:
                # Zeilenanzeige printen
                print(str(int((x-1)/2)) + "\t", end="")
            else:
                print("\t", end="")
            for y in range(self.size*2+1):
                print(buffer[x][y], end="")
            print("")

    def getTileAt(self, x:int, y:int) -> Room:
        room: Room
        for room in self.getMapTiles():
            if room.x == x and room.y == y:
                return room
        
        raise ValueError("No such room")
    
    def tileExists(self, x:int, y:int) -> bool:
        room: Room
        for room in self.getMapTiles():
            if room.x == x and room.y == y:
                return True
        return False
    
    def getStartingTile(self) -> Room:
        genX = int(self.size / 2)
        genY = int(self.size / 2)
        return self.getTileAt(genX, genY)

    # gibt alle Nachbar-Räume eines Raums zurück die mit dem Raum "tile" Verbunden sind
    def getNeighbouringTilesWithConnection(self, tile: Room) -> list[Room]:
        neighbours = []
        
        for i in range(8):
            shift = (1 << i) & 0b11111111
            if shift & tile.connections != 0:
                xOffset, yOffset = getPositionOffsetByDirection(i)
                
                neighbours.append(self.getTileAt(tile.x + xOffset, tile.y + yOffset))
                
        return neighbours
    
    def getNeighbouringTiles(self, tile: Room) -> list[Room]:
        neighbours = []
        
        for i in range(8):
            xOffset, yOffset = getPositionOffsetByDirection(i)
            if self.tileExists(xOffset, yOffset):
                neighbours.append(self.getTileAt(tile.x + xOffset, tile.y + yOffset))
                
        return neighbours
    
    def isGameWon(self) -> bool:
        win = True
        for room in self.getMapTiles():
            if not room.isDangerous and not room.isRevealed:
                win = False
        return win
