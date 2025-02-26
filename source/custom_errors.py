
class TilesNotNearbyError(Exception):
    """
        Exception wenn Tiles nicht nebeneinander sind
    """

    def __init__(self):
        super().__init__("Tiles are not nearby!")


class TilesCorrespondError(Exception):
    """
        Exception wenn Tiles die selbe Position haben
    """

    def __init__(self):
        super().__init__("Tiles have the same position!")