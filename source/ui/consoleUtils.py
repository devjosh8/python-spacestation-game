""" Helfer-Funktionen für die Konsole, darunter clearen und Farben """
import os
from .userInput import UserMode

GREETER = """
 ______    _______  __   __  __   __  _______  _______  __   __  ___   _______  _______ 
|    _ |  |   _   ||  | |  ||  |_|  ||       ||       ||  | |  ||   | |       ||       |
|   | ||  |  |_|  ||  | |  ||       ||  _____||       ||  |_|  ||   | |    ___||    ___|
|   |_||_ |       ||  |_|  ||       || |_____ |       ||       ||   | |   |___ |   |___ 
|    __  ||       ||       ||       ||_____  ||      _||       ||   | |    ___||    ___|
|   |  | ||   _   ||       || ||_|| | _____| ||     |_ |   _   ||   | |   |    |   |    
|___|  |_||__| |__||_______||_|   |_||_______||_______||__| |__||___| |___|    |___|    
"""

GREETER2 = """
 _______  _______  _______  __    _  _______  _______  __   __  _______  ______   
|   _   ||  _    ||       ||  |  | ||       ||       ||  | |  ||       ||    _ |  
|  |_|  || |_|   ||    ___||   |_| ||_     _||    ___||  | |  ||    ___||   | ||  
|       ||       ||   |___ |       |  |   |  |   |___ |  |_|  ||   |___ |   |_||_ 
|       ||  _   | |    ___||  _    |  |   |  |    ___||       ||    ___||    __  |
|   _   || |_|   ||   |___ | | |   |  |   |  |   |___ |       ||   |___ |   |  | |
|__| |__||_______||_______||_|  |__|  |___|  |_______||_______||_______||___|  |_|
"""

class Color():
    """ Color-Klasse für Konsolenfarben """
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    underline = '\033[4m'
    reset = '\033[0m'
    bold = '\033[1m'

def clearConsole() -> None:
    os.system('clear')

def printGreeter() -> None:
    print()
    print(GREETER) # Greeter printen in die Konsole
    print()
    
def printLegend(userMode: UserMode, jokerAmount: int) -> None:
    """ Druckt die Legende auf die Konsole; userMode ist der aktuelle userModue und jokerAmount 
        die aktuelle Anzahl an Joker """
    print("" + Color.green + "#" + Color.reset + ": Sicher\t"
          + Color.red + "#" + Color.reset + ": Markierung\t", end="")
    printUserMode(userMode)
    print("\tJoker: " + Color.yellow + str(jokerAmount) + Color.reset)
    
def printUserMode(userMode: UserMode) -> None:
    """ Druckt den userMode auf die Konsole """
    if userMode == UserMode.MARK:  
        print("\tAktiver Modus: " + Color.red + "Markieren" + Color.reset, end="")
    if userMode == UserMode.SCAN:  
        print("\tAktiver Modus: " + Color.green + "Scannen" + Color.reset, end="")
    
