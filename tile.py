from p5 import *
from mapdata import *

tilewidth = SIMW / GRIDDIMX
tileheight = SIMH / GRIDDIMY
wall_width_prop = 0.2 # ratio of wall thickness to tile size


class Tile:

    # type determines which pattern each tile will get
    # types: vertical, horizontal, cross, upleft, downleft, upright, downright, filled, t_up, t_down, t_left, t_right

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
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth * wall_width_prop, tileheight)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight)

        if self.type == "horizontal":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth, tileheight * wall_width_prop)

        if self.type == "filled":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight)

        if self.type == "upleft":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth, tileheight * wall_width_prop)

        if self.type == "upright":
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth * wall_width_prop, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth, tileheight * wall_width_prop)

        if self.type == "downleft":
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight * wall_width_prop)

        if self.type == "downright":
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth * wall_width_prop, tileheight)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight * wall_width_prop)

        if self.type == "cross":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth * wall_width_prop, tileheight * wall_width_prop) # tl, bl, tr, br
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)

        if self.type == "t_up":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth * wall_width_prop,tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth, tileheight * wall_width_prop)

        if self.type == "t_down":
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth, tileheight * wall_width_prop)

        if self.type == "t_left":
            rect((self.gridx * tilewidth, self.gridy * tileheight), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth, self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight)

        if self.type == "t_right":
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx * tilewidth + tilewidth * (1 - wall_width_prop), self.gridy * tileheight + tileheight * (1 - wall_width_prop)), tilewidth * wall_width_prop, tileheight * wall_width_prop)
            rect((self.gridx, self.gridy), tilewidth * wall_width_prop, tileheight)

    # determines if a point is within the track wall
    def isCollision(self, point):
        print("hello")