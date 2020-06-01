from p5 import *
from mapdata import *

wall_width_prop = 0.2 # ratio of wall thickness to tile size

# dictionary; keys = type strings, elements = .txt format version
to_text_file = {"vertical" : "v", "horizontal" : "h",
                 "upleft" : "ul", "downleft" : "dl", "upright" : "ur", "downright" : "dr",
                 "t_up" : "tu", "t_down" : "td", "t_left" : "tl", "t_right" : "tr",
                 "filled" : "f", "cross" : "c", "start" : "s", "end" : "e"}

# dictionary; keys = .txt format version, elements = type strings
to_tile_text = {"v" : "vertical", "h" : "horizontal",
                "ul" : "upleft", "dl" : "downleft", "ur" : "upright", "dr" : "downright",
                "tu" : "t_up", "td" : "t_down", "tl" : "t_left", "tr" : "t_right",
                "f" : "filled", "c" : "cross", "s" : "start", "e" : "end"}


class Tile:

    # type determines which pattern each tile will get
    # types: vertical, horizontal, cross, upleft, downleft, upright, downright, filled, t_up, t_down, t_left, t_right

    def __init__(self, gridx, gridy, type, dimx=GRIDDIMX, dimy=GRIDDIMY):
        self.gridx = gridx
        self.gridy = gridy
        self.type = type
        self.is_start = False
        self.is_goal = False
        self.tilewidth = SIMW / dimx
        self.tileheight = SIMH / dimy


    def set_type(self, type):
        self.type = type


    def get_type_for_file(self):
        return to_text_file[self.type]

    @staticmethod
    def get_type_from_file(filetext):
        return to_tile_text[filetext]

    # draws the tile
    def show(self):
        if self.is_start:
            fill('red')
        elif self.is_goal:
            fill('green')
        else:
            fill("black")

        if self.type == "start" or self.type == "end":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth, self.tileheight)

        if self.type == "vertical":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight)

        if self.type == "horizontal":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth, self.tileheight * wall_width_prop)

        if self.type == "filled":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth, self.tileheight)

        if self.type == "upleft":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth, self.tileheight * wall_width_prop)

        if self.type == "upright":
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth, self.tileheight * wall_width_prop)

        if self.type == "downleft":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth, self.tileheight * wall_width_prop)

        if self.type == "downright":
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth, self.tileheight * wall_width_prop)

        if self.type == "cross":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop) # tl, bl, tr, br
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)

        if self.type == "t_up":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth * wall_width_prop,self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth, self.tileheight * wall_width_prop)

        if self.type == "t_down":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth, self.tileheight * wall_width_prop)

        if self.type == "t_left":
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth, self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight)

        if self.type == "t_right":
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx * self.tilewidth + self.tilewidth * (1 - wall_width_prop), self.gridy * self.tileheight + self.tileheight * (1 - wall_width_prop)), self.tilewidth * wall_width_prop, self.tileheight * wall_width_prop)
            rect((self.gridx, self.gridy), self.tilewidth * wall_width_prop, self.tileheight)


    # determines if a point is within the track wall
    def isCollision(self, point):
        print("hello")