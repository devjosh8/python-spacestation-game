""" ist für den User-Input verantwortlich und gibt diesen über ein Result zurück """

from __future__ import annotations
from enum import Enum

class UserMode(Enum):
    """ Enum für die verschiedenen Modi die es beim User-Input gibt """
    SCAN = 0
    MARK = 1

class UserInputResultType(Enum):
    """ Enum für die Art, die ein InputResult haben kann """
    CHANGE_MODE = 0
    REVEAL_ROOM = 1
    JOKER_ROOM = 2
    
class UserInputResult():
    """ Das tatsächliche Ergebnis eines UserInputs, zusammengefasst in einer Klasse """
    def __init__(self, userInputResult: UserInputResultType, revealX: int=0, revealY: int=0) -> None:
        self.type = userInputResult
        self.revealX = revealX
        self.revealY = revealY
        if not (isinstance(revealX, int) and isinstance(revealY, int)):
            raise ValueError("X and Y Reveal coordinates must be valid interger values")
    

def getIntegerInput(prompt: str, minValue: int, maxValue: int) -> int:
    while True:
        print(prompt, end="")
        
        try:
            userInput = input()
            if userInput == "x":
                return -1
            
            userInputInt = int(userInput)
            
            if minValue <= userInputInt <= maxValue:
                return userInputInt
            
            print(f"Bitte eine Zahl im Bereich zwischen {minValue} und {maxValue} angeben!")
                
        except ValueError:
            print("Bitte eine valide Zahl eingeben!")

        
        
# Argumente: 
# userInputColor: Akzentfarbe für Userinput
# resetColor: Farbe zum Zurücksetzen der Farbe
# mapSize: Größe der Karte für richtige Integer-Erkennung   
def handleUserInput(userInputColor: str, resetColor: str, mapSize: int) -> UserInputResult | None:
    c = userInputColor # für bessere Lesbarkeit im folgenden Code
    r = resetColor
    print("\n'" + c + "m" + r + "' für Moduswechsel \t'" + c + "Enter" + r + "' für Koordinateneingabe" + r)
    userInput: str = input()
    if userInput.lower() == "m":
        return UserInputResult(UserInputResultType.CHANGE_MODE)
    
    if userInput == "":
        print("Geben Sie hintereinander eine Zeilenzahl und eine Spaltenzahl ein. '" + c + "x" + r + "' zum Abbrechen.")
        
        yCoord = getIntegerInput("Zeilenzahl: ", 0, mapSize-1)
        
        # wenn abgebrochen wurde
        if yCoord == -1:
            return None
        
        xCoord = getIntegerInput("Spaltenzahl: ", 0, mapSize-1)
        
        # wenn abgebrochen wurde
        if xCoord == -1:
            return None
        
        xCoordCopy = xCoord
        yCoordCopy = yCoord
        return UserInputResult(UserInputResultType.REVEAL_ROOM, revealX=xCoordCopy, revealY=yCoordCopy)
    
    # Joker einbauen
    if userInput == "j":
        print("Sie haben den JOKER ausgewählt. Geben Sie Zeilenzahl und Spaltenzahl des Raumes ein, über welchen Sie Informationen haben möchten. '"
              + c + "x" + r + "' zum Abbrechen.")
        yCoord = getIntegerInput("Zeilenzahl Joker: ", 0, mapSize-1)
        
        # wenn abgebrochen wurde
        if yCoord == -1:
            return None
        
        xCoord = getIntegerInput("Spaltenzahl Joker: ", 0, mapSize-1)
        
        # wenn abgebrochen wurde
        if xCoord == -1:
            return None
        
        xCoordCopy = xCoord
        yCoordCopy = yCoord
        return UserInputResult(UserInputResultType.JOKER_ROOM, revealX=xCoordCopy, revealY=yCoordCopy)
    return None
