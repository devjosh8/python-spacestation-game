"""
        Exception wenn Tiles nicht nebeneinander sind
"""
class TilesNotNearbyError(Exception):
    
    def __init__(self):
        super().__init__("Tiles are not nearby!")


"""
        Exception wenn Tiles die selbe Position haben
"""
class TilesCorrespondError(Exception):
    

    def __init__(self):
        super().__init__("Tiles have the same position!")