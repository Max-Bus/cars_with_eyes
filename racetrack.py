from tile import Tile
import numpy as np
from p5 import *
from mapdata import *


class RaceTrack:

    def __init__(self, grid=None, start=None, end=None):
        if (grid == None or start == None or end == None):
            g = [[None for x in range(GRIDDIMX)] for y in range(GRIDDIMY)]  # null gridd
            s = (int(np.random.randint(0, GRIDDIMX)), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid start
            e = (np.random.randint(0, GRIDDIMX), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid end

            # repick start and end if too close to each other
            while (distance((s[0], s[1]), (e[0], e[1])) < (GRIDDIMY + GRIDDIMX) / 2):
                s = (int(np.random.randint(0, GRIDDIMX)), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid start
                e = (np.random.randint(0, GRIDDIMX), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid end

            self.start = s
            self.end = e

            # possible transitions
            transitions = ["up", "down", "left", "right"]

            def addtrack(track=g, currx=s[0], curry=s[1], dir_to_prev=""):
                allowed_transitions = transitions.copy()

                # remove transitions that will go off the screen
                if currx == 0:
                    allowed_transitions.remove("left")
                if currx == GRIDDIMX - 1:
                    allowed_transitions.remove("right")
                if curry == 0:
                    allowed_transitions.remove("up")
                if curry == GRIDDIMY - 1:
                    allowed_transitions.remove("down")

                # remove the previously visited tile to avoid backtracking
                if dir_to_prev in allowed_transitions:
                    allowed_transitions.remove(dir_to_prev)

                rand_transition = allowed_transitions[np.random.randint(0, len(allowed_transitions))]

                nextx, nexty = currx, curry
                # the direction towards the current tile, from perspective of the next tile
                # find coordinates of next tile
                to_previous = ""
                if rand_transition == "up":
                    to_previous = "down"
                    nexty -= 1
                elif rand_transition == "down":
                    to_previous = "up"
                    nexty += 1
                elif rand_transition == "left":
                    to_previous = "right"
                    nextx -= 1
                elif rand_transition == "right":
                    to_previous = "left"
                    nextx += 1

                newtiletype = ""
                horizontals = ["left", "right"]
                verticals = ["up", "down"]
                if track[currx][curry] is None:
                    # continue going same direction
                    if rand_transition in verticals and dir_to_prev in verticals:
                        newtiletype = "vertical"
                    if rand_transition in horizontals and dir_to_prev in horizontals:
                        newtiletype = "horizontal"

                    # change direction
                    if rand_transition in verticals and dir_to_prev in horizontals:
                        newtiletype = rand_transition + dir_to_prev
                    if rand_transition in horizontals and dir_to_prev in verticals:
                        newtiletype = dir_to_prev + rand_transition

                    # add the tile for the first time
                    track[currx][curry] = Tile(currx, curry, newtiletype)

                # what to do if a tile is already existing
                else:
                    ttype = track[currx][curry].type

                    # currently vertical or horizontal
                    if ttype == "vertical":
                        if dir_to_prev == "left" or rand_transition == "left":
                            newtiletype = "t_left"
                        if dir_to_prev == "right" or rand_transition == "right":
                            newtiletype = "t_right"

                    if ttype == "horizontal":
                        if dir_to_prev == "up" or rand_transition == "up":
                            newtiletype = "t_up"
                        if dir_to_prev == "down" or rand_transition == "down":
                            newtiletype = "t_down"

                    # currently L-shaped
                    if ttype == "upleft":
                        if dir_to_prev == "down" or rand_transition == "down":
                            newtiletype = "t_left"
                        if dir_to_prev == "right" or rand_transition == "right":
                            newtiletype = "t_up"

                    if ttype == "downleft":
                        if dir_to_prev == "up" or rand_transition == "up":
                            newtiletype = "t_left"
                        if dir_to_prev == "right" or rand_transition == "right":
                            newtiletype = "t_down"

                    if ttype == "upright":
                        if dir_to_prev == "down" or rand_transition == "down":
                            newtiletype = "t_right"
                        if dir_to_prev == "left" or rand_transition == "left":
                            newtiletype = "t_up"

                    if ttype == "downright":
                        if dir_to_prev == "up" or rand_transition == "up":
                            newtiletype = "t_right"
                        if dir_to_prev == "left" or rand_transition == "left":
                            newtiletype = "t_down"

                    # currently T-shaped
                    if ttype == "t_up":
                        if dir_to_prev == "down" or rand_transition == "down":
                            newtiletype = "cross"

                    if ttype == "t_down":
                        if dir_to_prev == "up" or rand_transition == "up":
                            newtiletype = "cross"

                    if ttype == "t_left":
                        if dir_to_prev == "right" or rand_transition == "right":
                            newtiletype = "cross"

                    if ttype == "t_right":
                        if dir_to_prev == "left" or rand_transition == "left":
                            newtiletype = "cross"

                    # change the type of the tile if there is a change to be made
                    if newtiletype != "":
                        track[currx][curry].set_type(newtiletype)

                # path has reached the goal
                if currx == e[0] and curry == e[1]:
                    return True

                return addtrack(track, nextx, nexty, to_previous)

            # keep trying grid until it works
            is_success = addtrack()
            while not is_success:
                is_success = addtrack()

            # any empty tiles will become filled
            for col in range(0, GRIDDIMX):
                for row in range(0, GRIDDIMY):
                    if g[col][row] is None:
                        g[col][row] = Tile(col, row, "filled")

            g[s[0]][s[1]] = Tile(s[0], s[1], "filled")
            g[s[0]][s[1]].set_start()
            g[e[0]][e[1]].set_goal()
            self.grid = g

        else:
            self.grid = grid
            self.end = end
            self.start = start

    def display(self):
        for col in self.grid:
            for tl in col:
                tl.show()