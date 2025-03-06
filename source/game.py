from map.spaceshipMap import *
from ui.printingUtil import *
from ui.consoleUtils import *

def start():
    clearConsole()
    print("Bitte spielen Sie das Spiel nur in einem großen Terminal! Drücken Sie eine Taste, um das Spiel zu starten...")
    input()
    
    printGreeter()
    input()
    
    gameMap = Map(10)
    gameMap.generateMap()
    
    gameLoop(gameMap)


    
def gameLoop(gameMap: Map):
    shouldExit = False 
    
    scannedRooms = [] # eine Liste, die alle gescannten Räume enthält -> gescannte Räume werden grün
    
    while not shouldExit:
    
        colors = {}

        room: Room
        for room in scannedRooms:
            colors[(room.x, room.y)] = (Color.GREEN)
    #for neighbour in gameMap.getNeighbouringTilesWithConnection(gameMap.getStartingTile()):
    #    colors[( neighbour.x, neighbour.y )] = Color.GREEN
    
        gameMap.print(colors=colors, defaultColor=Color.RESET, safeColor=Color.GREEN)
        printLegend()
        input()
    