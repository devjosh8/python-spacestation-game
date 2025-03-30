import unittest

from source.map.mapHelper import getDirectionByPositionOffset, getPositionOffsetByDirection, getTextCharacterByDirection

class TestMapHelper(unittest.TestCase):
    def test_get_position_offset_by_direction(self):
        """Testet, ob getPositionOffsetByDirection die richtigen Koordinaten zurückgibt."""
        
        # Teste alle Richtungen
        self.assertEqual(getPositionOffsetByDirection(0), (0, -1))
        self.assertEqual(getPositionOffsetByDirection(1), (1, -1))
        self.assertEqual(getPositionOffsetByDirection(2), (1, 0))
        self.assertEqual(getPositionOffsetByDirection(3), (1, 1))
        self.assertEqual(getPositionOffsetByDirection(4), (0, 1))
        self.assertEqual(getPositionOffsetByDirection(5), (-1, 1))
        self.assertEqual(getPositionOffsetByDirection(6), (-1, 0))
        self.assertEqual(getPositionOffsetByDirection(7), (-1, -1))
        
        # Teste ungültigen Input
        with self.assertRaises(ValueError):
            getPositionOffsetByDirection(8)
            
    def test_get_direction_by_position_offset(self):
        """Testet, ob getDirectionByPositionOffset den richtigen Richtungsindex zurückgibt."""
        
        # Teste alle Positionen
        self.assertEqual(getDirectionByPositionOffset((0, -1)), 0)
        self.assertEqual(getDirectionByPositionOffset((1, -1)), 1)
        self.assertEqual(getDirectionByPositionOffset((1, 0)), 2)
        self.assertEqual(getDirectionByPositionOffset((1, 1)), 3)
        self.assertEqual(getDirectionByPositionOffset((0, 1)), 4)
        self.assertEqual(getDirectionByPositionOffset((-1, 1)), 5)
        self.assertEqual(getDirectionByPositionOffset((-1, 0)), 6)
        self.assertEqual(getDirectionByPositionOffset((-1, -1)), 7)
        
        # Teste ungültigen Input
        with self.assertRaises(ValueError):
            getDirectionByPositionOffset((0, 2))  # Keine gültige Richtung

    def test_get_text_character_by_direction(self):
        """Testet, ob getTextCharacterByDirection den richtigen Textcharakter zurückgibt."""
        
        # Teste alle Richtungen
        self.assertEqual(getTextCharacterByDirection(0), "|")
        self.assertEqual(getTextCharacterByDirection(1), "/")
        self.assertEqual(getTextCharacterByDirection(2), "-")
        self.assertEqual(getTextCharacterByDirection(3), "\\")
        self.assertEqual(getTextCharacterByDirection(4), "|")
        self.assertEqual(getTextCharacterByDirection(5), "/")
        self.assertEqual(getTextCharacterByDirection(6), "-")
        self.assertEqual(getTextCharacterByDirection(7), "\\")
        
        # Teste ungültigen Input
        with self.assertRaises(ValueError):
            getTextCharacterByDirection(8)
