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
        self.is_start = False
        self.is_goal = False

    def set_start(self):
        self.is_start = True

    def set_goal(self):
        self.is_goal =  True

    def set_type(self, type):
        self.type = type

    # draws the tile
    def show(self):
        if self.is_start:
            fill('red')
        elif self.is_goal:
            fill('green')
        else:
            fill("black")

        if self.type == "vertical":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 5, tileheight)
            rect((self.gridx * tilewidth + 4 * tilewidth / 5, self.gridy * tileheight), tilewidth / 5, tileheight)

        if self.type == "horizontal":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight / 5)
            rect((self.gridx * tilewidth, self.gridy * tileheight + 4 * tileheight / 5), tilewidth, tileheight / 5)

        if self.type == "filled":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight)

        if self.type == "upleft":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 5, tileheight / 5)
            rect((self.gridx * tilewidth + 4 * tilewidth / 5, self.gridy * tileheight), tilewidth / 5, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight + 4 * tileheight / 5), tilewidth, tileheight / 5)

        if self.type == "upright":
            rect((self.gridx * tilewidth + 4 * tilewidth / 5, self.gridy * tileheight), tilewidth / 5, tileheight / 5)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 5, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight + 4 * tileheight / 5), tilewidth, tileheight / 5)

        if self.type == "downleft":
            rect((self.gridx * tilewidth, self.gridy * tileheight + 4 * tileheight / 5), tilewidth / 5, tileheight / 5)
            rect((self.gridx * tilewidth + 4 * tilewidth / 5, self.gridy * tileheight), tilewidth / 5, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight / 5)

        if self.type == "downright":
            rect((self.gridx * tilewidth + 4 * tilewidth / 5, self.gridy * tileheight + 4 * tileheight / 5), tilewidth / 5, tileheight / 5)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth / 5, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight / 5)

    # determines if a point is within the track wall
    def isCollision(self, point):
        print("hello")