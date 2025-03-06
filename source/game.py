from map.spaceshipMap import *
from ui.asciiArt import *
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
    
    colors = {
        ( gameMap.getStartingTile().x, gameMap.getStartingTile().y ): (Color.RED + Color.BOLD)
    }
    
    
    
    for neighbour in gameMap.getNeighbouringTilesWithConnection(gameMap.getStartingTile()):
        colors[( neighbour.x, neighbour.y )] = Color.GREEN
    
    gameMap.print(colors=colors, defaultColor=Color.RESET)
    