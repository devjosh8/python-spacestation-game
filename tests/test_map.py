import unittest
from unittest.mock import patch, MagicMock
from source.map.spaceshipMap import Map
from source.map.spaceshipRoom import Room

class TestMap(unittest.TestCase):


    def test_get_tile_at(self):
        """ Testet, ob getTileAt den richtigen Raum zurückgibt. """
        map = Map(5)
        room = Room(2, 3, False)
        map.addMapTile(room)

        # Teste, ob der Raum mit den Koordinaten (2, 3) korrekt zurückgegeben wird
        returned_room = map.getTileAt(2, 3)
        self.assertEqual(returned_room, room)

    def test_tile_exists(self):
        """ Testet, ob tileExists korrekt funktioniert. """
        map = Map(5)
        room = Room(2, 3, False)
        map.addMapTile(room)

        # Überprüfen, ob tileExists True zurückgibt
        self.assertTrue(map.tileExists(2, 3))

        # Überprüfen, ob tileExists False zurückgibt
        self.assertFalse(map.tileExists(0, 0))

    def test_get_neighbouring_tiles_with_connection(self):
        """ Testet, ob getNeighbouringTilesWithConnection benachbarte Räume korrekt zurückgibt. """
        map = Map(5)
        room1 = Room(2, 2, False)
        room2 = Room(3, 2, False)
        room1.connectRooms(room2)  # Räume verbinden
        map.addMapTile(room1)
        map.addMapTile(room2)

        # Nachbarn von room1 sollten room2 beinhalten
        neighbours = map.getNeighbouringTilesWithConnection(room1)
        self.assertIn(room2, neighbours)

    def test_is_game_won_all_revealed(self):
        """ Testet, ob isGameWon True zurückgibt, wenn alle nicht gefährlichen Räume aufgedeckt sind. """
        map = Map(5)
        room1 = Room(1, 1, False)
        room2 = Room(1, 2, False)
        room1.isRevealed = True
        room2.isRevealed = True
        map.addMapTile(room1)
        map.addMapTile(room2)

        # Spiel sollte gewonnen sein, wenn alle nicht gefährlichen Räume aufgedeckt sind
        self.assertTrue(map.isGameWon())

    def test_is_game_won_not_all_revealed(self):
        """ Testet, ob isGameWon False zurückgibt, wenn nicht alle nicht gefährlichen Räume aufgedeckt sind. """
        map = Map(5)
        room1 = Room(1, 1, False)
        room2 = Room(1, 2, False)
        room1.isRevealed = True
        room2.isRevealed = False
        map.addMapTile(room1)
        map.addMapTile(room2)

        # Spiel sollte nicht gewonnen sein, da room2 nicht aufgedeckt ist
        self.assertFalse(map.isGameWon())
        
    def test_is_game_won(self):
        """Testet, ob isGameWon korrekt prüft, ob das Spiel gewonnen wurde."""
        map = Map(5)
        
        # Füge einige Räume hinzu
        room1 = Room(2, 2, False)
        room2 = Room(2, 3, False)
        room3 = Room(3, 2, False)
        
        room1.isRevealed = True
        room2.isRevealed = True
        room3.isRevealed = True
        
        map.addMapTile(room1)
        map.addMapTile(room2)
        map.addMapTile(room3)
        
        # Das Spiel ist gewonnen, wenn alle nicht gefährlichen Räume aufgedeckt sind
        self.assertTrue(map.isGameWon())
        
        # Markiere einen Raum als nicht aufgedeckt
        room3.isRevealed = False
        
        self.assertFalse(map.isGameWon())  # Das Spiel sollte nicht gewonnen sein

    def test_remove_map_tile(self):
        """Testet, ob removeMapTile einen Raum korrekt entfernt."""
        map = Map(5)
        room = Room(2, 2, False)
        map.addMapTile(room)
        
        self.assertIn(room, map.getMapTiles())  # Raum sollte hinzugefügt worden sein
        map.removeMapTile(room)
        self.assertNotIn(room, map.getMapTiles())  # Raum sollte entfernt worden sein

    def test_get_neighbouring_tiles_with_connection(self):
        """Testet, ob getNeighbouringTilesWithConnection die richtigen Nachbarn zurückgibt."""
        map = Map(5)
        room1 = Room(2, 2, False)
        room2 = Room(2, 3, False)
        room3 = Room(3, 2, False)
        map.addMapTile(room1)
        map.addMapTile(room2)
        map.addMapTile(room3)
        
        room1.connectRooms(room2)  # Verbindet room1 und room2
        room1.connectRooms(room3)  # Verbindet room1 und room3
        
        neighbours = map.getNeighbouringTilesWithConnection(room1)
        
        self.assertIn(room2, neighbours)
        self.assertIn(room3, neighbours)
        self.assertNotIn(room1, neighbours)  # Room1 sollte nicht als Nachbar erscheinen


