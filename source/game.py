from map.spaceshipMap import *
from ui.asciiArt import *
from ui.consoleUtils import *
from time import sleep

def start():
    clearConsole()
    print("Bitte spielen Sie das Spiel nur in einem großen Terminal! Drücken Sie eine Taste, um das Spiel zu starten...")
    input()
    
    printGreeter()
    
    print("Spiel starten", end="", flush=True)
    print()
    for i in range(10):
        sleep(0.03)
        print(".", end="", flush=True)
    
    gameMap = Map(10)
    gameMap.generateMap()
    
    gameLoop(gameMap)
    
def gameLoop(gameMap: Map):
    shouldExit = False 
    
    colors = {
        ( gameMap.getStartingTile().x, gameMap.getStartingTile().y ): (Color.RED + Color.BOLD)
    }
    
    
    
    for neighbour in gameMap.getNeighbouringTilesWithConnection(gameMap.getStartingTile()):
        colors[( neighbour.x, neighbour.y )] = Color.GREEN
    
    for tile in gameMap.getMapTiles():
        for neighbour in gameMap.getNeighbouringTilesWithConnection(tile):
            print(str(tile.x) + ":" + str(tile.y) + " verbunden mit " + str(neighbour.x) + ":" + str(neighbour.y))
    
    gameMap.print(colors=colors, defaultColor=Color.RESET)
    