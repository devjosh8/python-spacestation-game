import unittest
from unittest.mock import patch

from source.ui.userInput import getIntegerInput, handleUserInput, UserInputResultType

class TestUserInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['10'])
    def test_get_integer_input_valid(self, mock_input):
        """Testet, ob getIntegerInput eine gültige Zahl korrekt verarbeitet."""
        result = getIntegerInput("Geben Sie eine Zahl ein: ", 1, 20)
        self.assertEqual(result, 10)
    
    @patch('builtins.input', side_effect=['x'])
    def test_get_integer_input_exit(self, mock_input):
        """Testet, ob getIntegerInput den Abbruch korrekt behandelt (Eingabe 'x')."""
        result = getIntegerInput("Geben Sie eine Zahl ein: ", 1, 20)
        self.assertEqual(result, -1)
    
    @patch('builtins.input', side_effect=['abc', '15'])
    def test_get_integer_input_invalid_then_valid(self, mock_input):
        """Testet, ob getIntegerInput ungültige Eingaben ignoriert und eine gültige Zahl akzeptiert."""
        result = getIntegerInput("Geben Sie eine Zahl ein: ", 1, 20)
        self.assertEqual(result, 15)
    
    @patch('builtins.input', side_effect=['25', '10'])
    def test_get_integer_input_out_of_range_then_valid(self, mock_input):
        """Testet, ob getIntegerInput eine Zahl außerhalb des Bereichs ignoriert und eine gültige Zahl akzeptiert."""
        result = getIntegerInput("Geben Sie eine Zahl ein: ", 1, 20)
        self.assertEqual(result, 10)


    @patch('builtins.input', side_effect=['m'])
    def test_handle_user_input_change_mode(self, mock_input):
        """Testet, ob handleUserInput den Moduswechsel korrekt verarbeitet."""
        result = handleUserInput("red", "reset", 10)
        self.assertEqual(result.type, UserInputResultType.CHANGE_MODE)
    
    @patch('builtins.input', side_effect=['', '5', '7'])
    @patch('builtins.print')
    def test_handle_user_input_reveal_room(self, mock_print, mock_input):
        """Testet, ob handleUserInput eine Raumaufdeckung korrekt verarbeitet."""
        result = handleUserInput("red", "reset", 10)
        self.assertEqual(result.type, UserInputResultType.REVEAL_ROOM)
        self.assertEqual(result.revealX, 7)
        self.assertEqual(result.revealY, 5)
    
    @patch('builtins.input', side_effect=['j', '3', '4'])
    @patch('builtins.print')
    def test_handle_user_input_joker_room(self, mock_print, mock_input):
        """Testet, ob handleUserInput den Joker korrekt verarbeitet."""
        result = handleUserInput("red", "reset", 10)
        self.assertEqual(result.type, UserInputResultType.JOKER_ROOM)
        self.assertEqual(result.revealX, 4)
        self.assertEqual(result.revealY, 3)
    
    @patch('builtins.input', side_effect=['x'])
    @patch('builtins.print')
    def test_handle_user_input_exit(self, mock_print, mock_input):
        """Testet, ob handleUserInput die Abbruch-Eingabe ('x') korrekt behandelt."""
        result = handleUserInput("red", "reset", 10)
        self.assertIsNone(result)
