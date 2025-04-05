""" enthält die obere Logik für das Spiel """
from map.spaceshipMap import Map
from ui.consoleUtils import Color, clearConsole, printGreeter, printLegend
from ui.userInput import UserInputResult, UserInputResultType, UserMode, handleUserInput

MAP_SIZE = 10


def start() -> None:
    clearConsole()
    print("Bitte spielen Sie das Spiel nur in einem großen Terminal! Drücken Sie eine Taste, um das Spiel zu starten...\n" + 
          "Das Spiel kann jederzeit mit der Tastenkombination STRG+C abgebrochen werden.")
    input()

    printGreeter()
    input()

    gameMap = Map(MAP_SIZE)
    gameMap.generateMap()

    gameLoop(gameMap)


def gameLoop(gameMap: Map) -> None:
    clearConsole()

    shouldExit = False
    userMode = UserMode.SCAN
    jokerAmount = 2
    gameWon = False

    while not shouldExit:
        clearConsole()

        gameMap.print(defaultColor=Color.reset, safeColor=Color.green, markColor=Color.red)
        printLegend(userMode, jokerAmount)

        userInputResult = handleUserInput(Color.yellow, Color.reset, MAP_SIZE)
        if userInputResult is not None:

            # Modus ändern
            if userInputResult.type == UserInputResultType.CHANGE_MODE:
                userMode = UserMode.SCAN if userMode == UserMode.MARK else UserMode.MARK

            elif userInputResult.type == UserInputResultType.REVEAL_ROOM:
                if handleScanOrReveal(userInputResult=userInputResult, gameMap=gameMap, userMode=userMode):
                    shouldExit = True
                input()

            elif userInputResult.type == UserInputResultType.JOKER_ROOM:
                if jokerAmount > 0:
                    success = jokerRoomInformation(userInputResult=userInputResult, gameMap=gameMap)
                    input()
                    if success:
                        jokerAmount -= 1
                else:
                    print("Du keine Joker mehr übrig.")
                    input()

            gameWon = gameMap.isGameWon()

            if gameWon:
                shouldExit = True

    print("\n\n\n\nDas Spiel ist vorbei!")
    if gameWon:
        print("\n\n" + Color.yellow + "DU HAST GEWONNEN!" + Color.reset)

# gibt True zurück, wenn der gescannte Raum eine Falle ist -> dann muss das Spiel enden
def handleScanOrReveal(userInputResult: UserInputResult, gameMap: Map, userMode: UserMode) -> bool:
    x, y = userInputResult.revealX, userInputResult.revealY
    if not gameMap.roomExists(x, y):
        print(f"Ein Raum in Zeile {y} an Spalte {x} existiert nicht!")
        return False

    room = gameMap.getRoomAt(x, y)
    if room.isRevealed:
        if userMode == UserMode.SCAN:
            print("Der Raum ist bereits aufgedeckt!")
        elif userMode == UserMode.MARK:
            print("Der Raum ist bereits aufgedeckt und kann nicht markiert werden.")
        return False
    
    if userMode == UserMode.SCAN:
        if room.isDangerous:
            print("Der aufgedeckte Raum enthält eine " + Color.red + Color.bold + "Falle!" + Color.reset)
            return True
        room.isRevealed = True
        print("Der Raum wurde aufgedeckt!")

    elif userMode == UserMode.MARK:
        
        room.isMarked = not room.isMarked
        if room.isMarked:
            print("Der Raum wurde markiert.")
        else:
            print("Der Raum ist jetzt nicht mehr markiert.")
    return False

# gibt True zurück, wenn der Scan erfolgreich war, dann muss ein Joker abgezogen werden
def jokerRoomInformation(userInputResult: UserInputResult, gameMap: Map) -> bool:
    xCoordinate = userInputResult.revealX
    yCoordinate = userInputResult.revealY
    if gameMap.roomExists(xCoordinate, yCoordinate):
        inputRoom = gameMap.getRoomAt(xCoordinate, yCoordinate)
        if inputRoom.isRevealed:
            print(f"Ein Raum in Zeile {yCoordinate} an Spalte {xCoordinate} ist bereits aufgedeckt.")
            return False
        print(f"JOKER: Der Raum in Zeile {yCoordinate} an Spalte {xCoordinate} ist {('eine Falle!' if inputRoom.isDangerous else 'ein sicherer Raum.')}")
        return True

    print(f"Ein Raum in Zeile {yCoordinate} an Spalte {xCoordinate} existiert nicht.")

    return False
