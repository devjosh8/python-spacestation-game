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
        self.rooms: list[Room] = [] # Speichert die ganzen Tiles, die die Map ausmachen
        self.dangerousRoomsPropability = dangerousRoomsPropability
    
    # Die Karte generieren
    def generateMap(self) -> None:
        generatedRooms = 0
        
        # in der Mitte der Karte anfangen
        genX = int(self.size / 2)
        genY = int(self.size / 2)
                
        newRoom = Room(genX, genY, False)
        self.addRoom(newRoom)

        while generatedRooms < 50:
            # zufälligen Raum auswählen
            selectedRoom:Room = random.choice(self.getRooms())
            # weitermachen, wenn alle Richtungen blockiert sind
            if selectedRoom.allConnectionsOccupied():
                continue
            
            # eine zufällige Richtung auswählen -> alle möglichen Richtungen sind 0 in der Bitmaske
            # alle Bits durchgehen und alle die 0 sind in eine Liste hinzufügen
            possibleDirections = [i for i in range(8) if (selectedRoom.connections & (1 << i)) == 0]
            randomDirection = random.choice(possibleDirections)
            xOffset, yOffset = getPositionOffsetByDirection(randomDirection)
            newX = selectedRoom.x + xOffset
            newY = selectedRoom.y + yOffset
            
            # neue Koordinaten validieren und gegebenenfalls neu versuchen
            if newX < 0 or newY < 0 or newX >= self.size or newY >= self.size:
                continue
                        
            # befindet sich an dieser Stelle bereits ein Tile?
            # wenn ja, beide Tiles verbinden und abbrechen
            roomFound = False
            for lookupRoom in self.getRooms():
                if lookupRoom.x == newX and lookupRoom.y == newY:
                    selectedRoom.connectRooms(lookupRoom)
                    roomFound = True
            
            if roomFound:
                continue
            
            # ansonsten neues Tile erstellen und mit dem aktuellen verbinden
            newRoom = Room(selectedRoom.x + xOffset, selectedRoom.y + yOffset)
            newRoom.connectRooms(selectedRoom)
            self.addRoom(newRoom)
                
            generatedRooms+=1
            
        self._removeRoomsWithSingleConnection()
        self._generateDangerousRooms()

    def _removeRoomsWithSingleConnection(self) -> None:
        roomWithSingleConnectionExist = True
        roomsToRemoveNextIteration: list[Room] = []
        while roomWithSingleConnectionExist:
            roomToRemove: Room
            for roomToRemove in roomsToRemoveNextIteration:
                neighbours = self.getNeighbouringRoomsWithConnection(roomToRemove)
                # Prämisse => roomToRemove hat nur einen Nachbar
                
                if len(neighbours) != 1:
                    raise ValueError("Map generation error: Room which is supposed to have only 1 neighbour has 0 or more than 1")
                
                for neighbouringRoom in neighbours:
                    roomToRemove.disconnectRooms(neighbouringRoom)
                
                self.removeRoom(roomToRemove)
            
            roomsToRemoveNextIteration.clear()
            
            roomWithSingleConnectionExist = False
            for room in self.getRooms():
                if room.getNumberOfConnections() == 1:
                    roomsToRemoveNextIteration.append(room)
                    roomWithSingleConnectionExist = True 

        
    def _generateDangerousRooms(self) -> None:
        # zufällig gefährliche Räume generieren
        room: Room
        for room in self.getRooms():
            if random.randint(0, int(1/self.dangerousRoomsPropability)) == 0:
                room.isDangerous = True

        # der Startraum ist in jedem Fall nicht gefährlich
        self.getStartingRoom().isDangerous = False

        # Für jeden Raum die Anzahl an gefährlichen Nachbarräumen setzen
        for room in self.getRooms():
            connectedRoom: Room
            dangerousNearbyRooms = 0
            for connectedRoom in self.getNeighbouringRoomsWithConnection(room):
                if connectedRoom.isDangerous:
                    dangerousNearbyRooms+=1
            room.dangerousNearbyRooms = dangerousNearbyRooms
            # Nur Räume, die nicht gefährlich sind, können schon gescannt sein!
            if not room.isDangerous and random.randint(0, 1) == 0:
                room.isRevealed = True
            
    def addRoom(self, tile: Room) -> None:
        self.rooms.append(tile)
        
    def removeRoom(self, tile: Room) -> None:
        self.rooms.remove(tile)
        
    def getRooms(self) -> list[Room]:
        return self.rooms
    
    
    def _createPrintBuffer(self, defaultColor:str ="", safeColor:str ="", markColor:str ="") -> list[list[str]]:
        """ erstellt den Printbuffer, gefüllt mit den Farben aus den Argumenten. """
        # Ein 2D Array erstellen mit den Dimensionen size * size initialisiert auf alles ' ' 
        # Wichtig!!! Im Buffer kommt zuerst die Y-Koordinate, dann die X Koordinate!
        # Einen Punkt . jeweils nur in jede zweite Spalte und Zeile platzieren, damit das Raster nicht voll mit Punkten ist
        # und für den User die Zusammenhänge zwischen Zeile und Spalte besser ersichtlich machen, statt einem Punkte spam
        buffer = [[("." if i % 2 != 0 and j % 2 != 0 else " ") for i in range(self.size * 2 + 1)] for j in range(self.size * 2 + 1)]

        # Durchlauf, um Räume und Farben zu platzieren
        room: Room
        for room in self.rooms:
            
            roomChar = "#"
            if room.isRevealed:
                roomChar = safeColor + str(room.dangerousNearbyRooms) + defaultColor
            
            elif room.isMarked:
                roomChar = markColor + "#" + defaultColor
            
            buffer[room.y*2+1][room.x*2+1] = roomChar
        
        # erster Durchlauf um die Wege zu platzieren
        for room in self.getRooms():
            for neighbor in self.getNeighbouringRoomsWithConnection(room):
                posOffsetX = neighbor.x - room.x
                posOffsetY = neighbor.y - room.y
                
                directionIndex = getDirectionByPositionOffset( (posOffsetX, posOffsetY) )
                char = getTextCharacterByDirection(directionIndex)
                
                buffer[room.y*2 + posOffsetY + 1][room.x*2 + posOffsetX + 1] = char 
                
        # zweiter Durchlauf, um Diagonalverbindungen richtig zu platzieren 
        # vorheriger Code hat ergeben, dass beide Schleifen NICHT in eine gepackt werden können
        # und seperat gehalten werden müssen!!
        for room in self.getRooms():
            for neighbor in self.getNeighbouringRoomsWithConnection(room):
                posOffsetX = neighbor.x - room.x
                posOffsetY = neighbor.y - room.y
                
                directionIndex = getDirectionByPositionOffset( (posOffsetX, posOffsetY) )
                char = getTextCharacterByDirection(directionIndex)
                if char == "/" and buffer[room.y*2+posOffsetY + 1][room.x*2+posOffsetX + 1] == "\\":
                    char = "X"
                    buffer[room.y*2 + posOffsetY + 1][room.x*2 + posOffsetX + 1] = char 
                if char == "\\" and buffer[room.y*2+posOffsetY + 1][room.x*2+posOffsetX + 1] == "/":
                    char = "X"
                    buffer[room.y*2 + posOffsetY + 1][room.x*2 + posOffsetX + 1] = char 
        return buffer
        
    def print(self, defaultColor:str ="", safeColor:str ="", markColor:str ="") -> None:
        """ druckt die Map auf die Konsole. Argumente sind hier die Standardfarbe (Resetcolor), Akzentfarbe von
            sicheren Räumen (safeColor) und Akzentfarbe von markierten Räumen (markColor)"""
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

    def getRoomAt(self, x:int, y:int) -> Room:
        room: Room
        for room in self.getRooms():
            if room.x == x and room.y == y:
                return room
        
        raise ValueError("No such room")
    
    def roomExists(self, x:int, y:int) -> bool:
        room: Room
        for room in self.getRooms():
            if room.x == x and room.y == y:
                return True
        return False
    
    def getStartingRoom(self) -> Room:
        """ gibt den Startraum einer Karte zurück, der in jedem Fall in der Mitte der Karte liegt und
            existieren muss """
        genX = int(self.size / 2)
        genY = int(self.size / 2)
        return self.getRoomAt(genX, genY)

    # gibt alle Nachbar-Räume eines Raums zurück die mit dem Raum "tile" Verbunden sind
    def getNeighbouringRoomsWithConnection(self, tile: Room) -> list[Room]:
        """ Gibt alle Nachbarräume eines Raums als Liste zurück, die mit dem Raum verbunden sind """
        neighbours = []
        
        for i in range(8):
            shift = (1 << i) & 0b11111111
            if shift & tile.connections != 0:
                xOffset, yOffset = getPositionOffsetByDirection(i)
                
                neighbours.append(self.getRoomAt(tile.x + xOffset, tile.y + yOffset))
                
        return neighbours
    
    def getNeighbouringRooms(self, tile: Room) -> list[Room]:
        """ Gibt alle Nachbarräume eines Raums zurück, unabhängig davon, ob die Räume
            verbunden sind oder nicht"""
        neighbours = []
        
        for i in range(8):
            xOffset, yOffset = getPositionOffsetByDirection(i)
            if self.roomExists(xOffset, yOffset):
                neighbours.append(self.getRoomAt(tile.x + xOffset, tile.y + yOffset))
                
        return neighbours
    
    def isGameWon(self) -> bool:
        """ testet ob das Spiel gewonnen ist. Verglichen wird hier, ob alle Räume
            die nicht gefährlich sind aufgedeckt sind oder nicht """
        win = True
        for room in self.getRooms():
            if not room.isDangerous and not room.isRevealed:
                win = False
        return win
