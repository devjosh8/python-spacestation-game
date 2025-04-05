""" Testet Methoden und Funktionen im Beziehung zu Räumen """

import unittest

from source.map.spaceshipRoom import Room, getBitByOffset
from source.map.spaceshipMap import Map
from source.map.customErrors import RoomsHaveOverlappingPositionError, RoomsNotNearbyError
from source.map.mapHelper import getTextCharacterByDirection

class TestRooms(unittest.TestCase):
    """ Testet Methoden und Funktionen im Beziehung zu Räumen """

    def test_room(self) -> None:
        """
        Testet das Erstellen von MapTiles, dabei sollten nur ganze Zahlen als
        x und y Koordinate (Integer) erlaubt sein
        """
        self.assertRaises(ValueError, Room, 0.1, 0, False)
        self.assertRaises(ValueError, Room, 0.1, 0.0000000000345654, False)
        self.assertRaises(ValueError, Room, 1, 10e7, False)
    
    def test_room_nearby(self) -> None:
        """
        Testet, ob Tiles die nebeneinander sind auch so erkannt werden
        """
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(1, 0, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(0, 1, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(-1, 0, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(0, -1, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(1, 1, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(-1, -1, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(-1, 1, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(1, -1, False)))
        self.assertTrue(Room(0, 0, False).roomsNearby(Room(0, 0, False)))
        
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(0, 2, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(0, -2, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(-2, 0, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(2, 0, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(1, 2, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(2, -1, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(1, -2, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(0, 50, False)))
        self.assertFalse(Room(0, 0, False).roomsNearby(Room(1, 435, False)))
        
        
    def test_get_bit(self) -> None:
        """
        Testet, ob die Funktion getBit das richtige Bit zurückgibt, um die Position zwischen zwei
        Räumen korrekt zu verbinden (y wächst nach unten, x wächst nach rechts!) Siehe spaceShipMap
        """
        self.assertEqual(getBitByOffset(Room(0, 0, False), Room(0, 1, False)), 4)
        self.assertEqual(getBitByOffset(Room(5, 5, False), Room(6, 6, False)), 3)
        self.assertEqual(getBitByOffset(Room(345636, 10, False), Room(345637, 10, False)), 2)
        self.assertEqual(getBitByOffset(Room(0, 0, False), Room(1, -1, False)), 1)
        self.assertEqual(getBitByOffset(Room(6000, 3000, False), Room(6000, 3000-1, False)), 0)
        self.assertEqual(getBitByOffset(Room(0, 0, False), Room(-1, -1, False)), 7)
        self.assertEqual(getBitByOffset(Room(29457, 2456, False), Room(29457-1, 2456, False)), 6)
        self.assertEqual(getBitByOffset(Room(0, 0, False), Room(-1, 1, False)), 5)

        self.assertRaises(RoomsHaveOverlappingPositionError, getBitByOffset, Room(0, 0, False), Room(0, 0, False))
        
        self.assertRaises(RoomsNotNearbyError, getBitByOffset, Room(-9487346, 0, False), Room(-948734644, 0, False))
        self.assertRaises(RoomsNotNearbyError, getBitByOffset, Room(1000, 1000, False), Room(-1000, -1000, False))
    
    def test_tile_connection(self) -> None:
        """
            Integration-Test, ob die Funktionen miteinander richtig funktionieren. Es wird
            geprüft, ob die Tiles an der selben Position sind, wenn das nicht der Fall ist
            und die Tiles nebeneinander sind wird versucht, diese Tiles zu verbinden. Dann
            wird überprüft, ob diese beiden Tiles am Ende wirklich verbunden sind
        """
        for a in range(-10, 10):
            for b in range(-10, 10):
                for c in range(-10, 10):
                    for d in range(-10, 10):
                        m1 = Room(a, b, False)
                        m2 = Room(c, d, False)
                        if a == c and b == d:
                            self.assertRaises(RoomsHaveOverlappingPositionError, m1.connectedTo, m2)
                            self.assertRaises(RoomsHaveOverlappingPositionError, m2.connectedTo, m1)
                            continue
                        
                        self.assertFalse(m1.connectedTo(m2))
                        self.assertFalse(m2.connectedTo(m1))
                        
                        if m1.roomsNearby(m2):
                            m1.connectRooms(m2)
                            self.assertTrue(m1.connectedTo(m2))
                            self.assertTrue(m2.connectedTo(m1))
                            m2.disconnectRooms(m1)
                            self.assertFalse(m1.connectedTo(m2))
                            self.assertFalse(m2.connectedTo(m1))
                            
        map_room = Room(0, 0, False)
        
        self.assertFalse(map_room.allConnectionsOccupied())
        
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == y == 0: 
                    continue # Um die exception der gleichen Tiles zu verhindern
                m1 = Room(x, y, False)
                if map_room.roomsNearby(m1):
                    map_room.connectRooms(m1)
                    
        self.assertTrue(map_room.allConnectionsOccupied())
        
    def test_get_text_character_by_direction(self) -> None:
        """ testet, ob der Textcharakter richtig aus der Raumbeziehung erkannt wird """
        r1 = Room(0, 0, False)
        r2 = Room(1, 1, False)
        r3 = Room(-1, 0, False)
        r4 = Room(0, 1, False)
        r1.connectRooms(r2)
        r2.connectRooms(r3)
        
        self.assertEqual(getTextCharacterByDirection(getBitByOffset(r1, r2)), "\\")
        self.assertEqual(getTextCharacterByDirection(getBitByOffset(r1, r3)), "-")
        self.assertEqual(getTextCharacterByDirection(getBitByOffset(r3, r4)), "\\")
        self.assertEqual(getTextCharacterByDirection(getBitByOffset(r4, r1)), "|")
    
    def test_get_neighbouring_tiles(self) -> None:
        """ testet ob Nachbarräume richtig erkannt werden"""
        sp_map = Map(10)
        for x in range(10):
            for y in range(10):
                sp_map.addRoom(Room(x, y, False))
        
        sp_map.getRoomAt(5, 5).connectRooms(sp_map.getRoomAt(6, 6))
        self.assertTrue(sp_map.getRoomAt(6, 6) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(5, 6) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(6, 5) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(5, 4) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(4, 5) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(4, 6) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(3, 7) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        sp_map.getRoomAt(5, 5).connectRooms(sp_map.getRoomAt(4, 5))
        sp_map.getRoomAt(5, 5).connectRooms(sp_map.getRoomAt(6, 5))
        self.assertTrue(sp_map.getRoomAt(6, 6) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertTrue(sp_map.getRoomAt(4, 5) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertTrue(sp_map.getRoomAt(6, 5) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        
        self.assertFalse(sp_map.getRoomAt(5, 6) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(5, 4) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(4, 6) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
        self.assertFalse(sp_map.getRoomAt(3, 7) in sp_map.getNeighbouringRoomsWithConnection(sp_map.getRoomAt(5, 5)))
    
    def test_get_number_of_connections(self) -> None:
        """ testet, ob die Anzahl der Verbindungen richtig ist """
        tile = Room(0, 0)
        self.assertEqual(tile.getNumberOfConnections(), 0)
        tile1 = Room(1, 1)
        self.assertEqual(tile1.getNumberOfConnections(), 0)
        tile.connectRooms(tile1)
        self.assertEqual(tile.getNumberOfConnections(), 1)
        self.assertEqual(tile1.getNumberOfConnections(), 1)
