

# gibt die Richtung in eine Verbindung anhand der Nummer der Richtung zurück
# wichtig! Da  die Verbindung für den Buffer genutzt wird, ist die Y-Koordinate invertiert!
def getPositionOffsetByDirection(direction):
    match(direction):
        case 0:
            return (0, -1)
        case 1:
            return (1, -1)
        case 2:
            return (1, 0)
        case 3:
            return (1, 1)
        case 4:
            return (0, 1)
        case 5:
            return (-1, 1)
        case 6:
            return (-1, 0)
        case 7:
            return (-1, -1)
    raise ValueError("Directional number could not be converted into acutal coordinates")

def getDirectionIndexByPositionOffset(position):
    match(position):
        case (0, -1):
            return 0
        case (1, -1):
            return 1
        case (1, 0):
            return 2
        case (1, 1):
            return 3
        case (0, 1):
            return 4
        case (-1, 1):
            return 5
        case (-1, 0):
            return 6
        case (-1, -1):
            return 7
    raise ValueError("Offset coordinates could not be converted into direction index")

# gibt den richtigen Text-Charakter für einen gesetzten Bit in der connections-Bit-Maske
# eines Rooms zurück (siehe spaceshipRoom.py)
def getTextCharacterByDirection(direction):
    match(direction):
        case 0:
            return "|"
        case 1:
            return "/"
        case 2:
            return "-"
        case 3:
            return "\\"
        case 4:
            return "|"
        case 5:
            return "/"
        case 6:
            return "-"
        case 7:
            return "\\"
    raise ValueError("Directional number could not be converted into text symbol")