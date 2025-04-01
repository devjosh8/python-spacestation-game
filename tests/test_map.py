""" Testet Methoden und Funktionen im Beziehung zur spaceship-Map """

import unittest
from source.map.spaceshipMap import Map
from source.map.spaceshipRoom import Room

class TestMap(unittest.TestCase):
    """ Testet Methoden und Funktionen im Beziehung zur spaceship-Map """

    def test_get_tile_at(self) -> None:
        """ Testet, ob getTileAt den richtigen Raum zurückgibt. """
        map = Map(5)
        room = Room(2, 3, False)
        map.addRoom(room)

        # Teste, ob der Raum mit den Koordinaten (2, 3) korrekt zurückgegeben wird
        returned_room = map.getRoomAt(2, 3)
        self.assertEqual(returned_room, room)

    def test_tile_exists(self) -> None:
        """ Testet, ob tileExists korrekt funktioniert. """
        map = Map(5)
        room = Room(2, 3, False)
        map.addRoom(room)

        # Überprüfen, ob tileExists True zurückgibt
        self.assertTrue(map.roomExists(2, 3))

        # Überprüfen, ob tileExists False zurückgibt
        self.assertFalse(map.roomExists(0, 0))

    def test_get_neighbouring_tiles_with_connection(self) -> None:
        """ Testet, ob getNeighbouringTilesWithConnection benachbarte Räume korrekt zurückgibt. """
        map = Map(5)
        room1 = Room(2, 2, False)
        room2 = Room(3, 2, False)
        room1.connectRooms(room2)  # Räume verbinden
        map.addRoom(room1)
        map.addRoom(room2)

        # Nachbarn von room1 sollten room2 beinhalten
        neighbours = map.getNeighbouringRoomsWithConnection(room1)
        self.assertIn(room2, neighbours)

    def test_is_game_won_all_revealed(self) -> None:
        """ Testet, ob isGameWon True zurückgibt, wenn alle nicht gefährlichen Räume aufgedeckt sind. """
        map = Map(5)
        room1 = Room(1, 1, False)
        room2 = Room(1, 2, False)
        room1.isRevealed = True
        room2.isRevealed = True
        map.addRoom(room1)
        map.addRoom(room2)

        # Spiel sollte gewonnen sein, wenn alle nicht gefährlichen Räume aufgedeckt sind
        self.assertTrue(map.isGameWon())

    def test_is_game_won_not_all_revealed(self) -> None:
        """ Testet, ob isGameWon False zurückgibt, wenn nicht alle nicht gefährlichen Räume aufgedeckt sind. """
        map = Map(5)
        room1 = Room(1, 1, False)
        room2 = Room(1, 2, False)
        room1.isRevealed = True
        room2.isRevealed = False
        map.addRoom(room1)
        map.addRoom(room2)

        # Spiel sollte nicht gewonnen sein, da room2 nicht aufgedeckt ist
        self.assertFalse(map.isGameWon())
        
    def test_is_game_won(self) -> None:
        """Testet, ob isGameWon korrekt prüft, ob das Spiel gewonnen wurde."""
        map = Map(5)
        
        # Füge einige Räume hinzu
        room1 = Room(2, 2, False)
        room2 = Room(2, 3, False)
        room3 = Room(3, 2, False)
        
        room1.isRevealed = True
        room2.isRevealed = True
        room3.isRevealed = True
        
        map.addRoom(room1)
        map.addRoom(room2)
        map.addRoom(room3)
        
        # Das Spiel ist gewonnen, wenn alle nicht gefährlichen Räume aufgedeckt sind
        self.assertTrue(map.isGameWon())
        
        # Markiere einen Raum als nicht aufgedeckt
        room3.isRevealed = False
        
        self.assertFalse(map.isGameWon())  # Das Spiel sollte nicht gewonnen sein

    def test_remove_map_tile(self) -> None:
        """Testet, ob removeMapTile einen Raum korrekt entfernt."""
        map = Map(5)
        room = Room(2, 2, False)
        map.addRoom(room)
        
        self.assertIn(room, map.getRooms())  # Raum sollte hinzugefügt worden sein
        map.removeRoom(room)
        self.assertNotIn(room, map.getRooms())  # Raum sollte entfernt worden sein

    def test_get_neighbouring_tiles_with_connection2(self) -> None:
        """Testet, ob getNeighbouringTilesWithConnection die richtigen Nachbarn zurückgibt."""
        map = Map(5)
        room1 = Room(2, 2, False)
        room2 = Room(2, 3, False)
        room3 = Room(3, 2, False)
        map.addRoom(room1)
        map.addRoom(room2)
        map.addRoom(room3)
        
        room1.connectRooms(room2)  # Verbindet room1 und room2
        room1.connectRooms(room3)  # Verbindet room1 und room3
        
        neighbours = map.getNeighbouringRoomsWithConnection(room1)
        
        self.assertIn(room2, neighbours)
        self.assertIn(room3, neighbours)
        self.assertNotIn(room1, neighbours)  # Room1 sollte nicht als Nachbar erscheinen
