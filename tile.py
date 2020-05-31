from p5 import *
from mapdata import *

tilewidth = SIMW / GRIDDIMX
tileheight = SIMH / GRIDDIMY

class Tile:

    # type determines which pattern each tile will get
    # types: vertical, horizontal, cross, upleft, downleft, upright, downright, filled

    def __init__(self, gridx, gridy, type):
        self.gridx = gridx
        self.gridy = gridy
        self.type = type

    # draws the tile
    def show(self):
        fill("black")
        if self.type == "vertical":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 4, tileheight)
            rect((self.gridx * tilewidth + 3 * tilewidth / 4, self.gridy * tileheight), tilewidth / 4, tileheight)

        if self.type == "horizontal":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight / 4)
            rect((self.gridx * tilewidth, self.gridy * tileheight + 3 * tileheight / 4), tilewidth, tileheight / 4)

        if self.type == "filled":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight)

        if self.type == "upleft":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 4, tileheight / 4)
            rect((self.gridx * tilewidth + 3 * tilewidth / 4, self.gridy * tileheight), tilewidth / 4, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight + 3 * tileheight / 4), tilewidth, tileheight / 4)

        if self.type == "upright":
            rect((self.gridx * tilewidth + 3 * tilewidth / 4, self.gridy * tileheight), tilewidth / 4, tileheight / 4)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 4, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight + 3 * tileheight / 4), tilewidth, tileheight / 4)

        if self.type == "downleft":
            rect((self.gridx * tilewidth, self.gridy * tileheight + 3 * tileheight / 4), tilewidth / 4, tileheight / 4)
            rect((self.gridx * tilewidth + 3 * tilewidth / 4, self.gridy * tileheight), tilewidth / 4, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight / 4)

        if self.type == "downright":
            rect((self.gridx * tilewidth + 3 * tilewidth / 4, self.gridy * tileheight + 3 * tileheight / 4), tilewidth / 4, tileheight / 4)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 4, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight / 4)

    # determines if a point is within the track wall
    def isCollision(self, point):
        print("hello")