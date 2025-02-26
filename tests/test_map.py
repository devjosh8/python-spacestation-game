import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from source.map import *

class TestInput(unittest.TestCase):
    
    """
        Testet das Erstellen von MapTiles, dabei sollten nur ganze Zahlen als
        x und y Koordinate (Integer) erlaubt sein
    """
    def test_maptile(self):
        self.assertRaises(ValueError, MapTile, 0.1, 0, False)
        self.assertRaises(ValueError, MapTile, 0.1, 0.0000000000345654, False)
        self.assertRaises(ValueError, MapTile, 1, 10e7, False)
    
    """
        Testet, ob Tiles die nebeneinander sind auch so erkannt werden
    """
    def test_maptile_nearby(self):
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(1, 0, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(0, 1, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(-1, 0, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(0, -1, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(1, 1, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(-1, -1, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(-1, 1, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(1, -1, False)))
        self.assertTrue(MapTile(0, 0, False).tilesNearby(MapTile(0, 0, False)))
        
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(0, 2, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(0, -2, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(-2, 0, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(2, 0, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(1, 2, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(2, -1, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(1, -2, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(0, 50, False)))
        self.assertFalse(MapTile(0, 0, False).tilesNearby(MapTile(1, 435, False)))
        
        
    """
        Testet, ob die Funktion getBit das richtige Bit zurückgibt
    """
    def test_get_bit(self):
        self.assertEqual(getBit(MapTile(0, 0, False), MapTile(0, 1, False)), 0)
        self.assertEqual(getBit(MapTile(5, 5, False), MapTile(6, 6, False)), 1)
        self.assertEqual(getBit(MapTile(345636, 10, False), MapTile(345637, 10, False)), 2)
        self.assertEqual(getBit(MapTile(0, 0, False), MapTile(1, -1, False)), 3)
        self.assertEqual(getBit(MapTile(6000, 3000, False), MapTile(6000, 3000-1, False)), 4)
        self.assertEqual(getBit(MapTile(0, 0, False), MapTile(-1, -1, False)), 5)
        self.assertEqual(getBit(MapTile(29457, 2456, False), MapTile(29457-1, 2456, False)), 6)
        self.assertEqual(getBit(MapTile(0, 0, False), MapTile(-1, 1, False)), 7)

        self.assertRaises(TilesCorrespondError, getBit, MapTile(0, 0, False), MapTile(0, 0, False))
        
        self.assertRaises(TilesNotNearbyError, getBit, MapTile(-9487346, 0, False), MapTile(-948734644, 0, False))
        self.assertRaises(TilesNotNearbyError, getBit, MapTile(1000, 1000, False), MapTile(-1000, -1000, False))
    
    """
        Integration-Test, ob die Funktionen miteinander richtig funktionieren. Es wird
        geprüft, ob die Tiles an der selben Position sind, wenn das nicht der Fall ist
        und die Tiles nebeneinander sind wird versucht, diese Tiles zu verbinden. Dann
        wird überprüft, ob diese beiden Tiles am Ende wirklich verbunden sind
    """
    def test_tile_connection(self):
        for a in range(-10, 10):
            for b in range(-10, 10):
                for c in range(-10, 10):
                    for d in range(-10, 10):
                        m1 = MapTile(a, b, False)
                        m2 = MapTile(c, d, False)
                        if a == c and b == d:
                            self.assertRaises(TilesCorrespondError, m1.connectedTo, m2)
                            self.assertRaises(TilesCorrespondError, m2.connectedTo, m1)
                            continue
                        self.assertFalse(m1.connectedTo(m2))
                        self.assertFalse(m2.connectedTo(m1))
                        
                        if m1.tilesNearby(m2):
                            m1.connectTiles(m2)
                            self.assertTrue(m1.connectedTo(m2))
                            self.assertTrue(m2.connectedTo(m1))