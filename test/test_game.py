""" Teste die game.py Hauptschleife und die Methoden """

import unittest
from source.game import jokerRoomInformation
from source.map.spaceshipMap import Map
from source.ui.userInput import UserInputResult, UserInputResultType

class TestGameLogic(unittest.TestCase):
    """ Teste die game.py Hauptschleife und die Methoden """

    def setUp(self) -> None:
        """ setup für die tests """
        # Map mit 10 -> daher gibt es immer einen Raum bei 5/5 (muss)
        self.map = Map(10)
        self.map.generateMap()

        self.assertIsNotNone(self.map.getRoomAt(5, 5))

    def test_joker_on_revealed_room_should_fail(self) -> None:
        """ Testet, ob die Methode die die Joker abzieht das richtige Ergebnis bringt """
        room = self.map.getRoomAt(5, 5)
        room.isRevealed = True
        input_result = UserInputResult(UserInputResultType.JOKER_ROOM, 5, 5)
        result = jokerRoomInformation(input_result, self.map)
        self.assertFalse(result)

    def test_joker_on_unscanned_room(self) -> None:
        """ Testet, ob die Methode die die Joker abzieht das richtige Ergebnis bringt """
        self.map.getRoomAt(5, 5).isDangerous = True
        self.map.getRoomAt(5, 5).isRevealed = False
        input_result = UserInputResult(UserInputResultType.JOKER_ROOM, 5, 5)
        result = jokerRoomInformation(input_result, self.map)
        self.assertTrue(result)
