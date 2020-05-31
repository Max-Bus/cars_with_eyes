from tile import Tile

class RaceTrack:

    def __init__(self, grid = None, start = None, end = None):
        if (grid == None or start == None or end == None):
            # self.grid = todo
            # self.start = () tuple todo
            # self.end = () tuple todo
            print("track")
        else:
            self.grid = grid
            self.end = end
            self.start = start

    def maketile(self):
        return Tile(3, 2, "vertical")


