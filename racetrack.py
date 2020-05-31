from tile import Tile
import numpy as np
from p5 import *
from mapdata import *

class RaceTrack:

    def __init__(self, grid = None, start = None, end = None):
        if (grid == None or start == None or end == None):
            g = [ [ None for x in range( GRIDDIMX ) ] for y in range(GRIDDIMY) ] # grid
            s = (int(np.random.randint(0, GRIDDIMX)), np.random.randint(0, GRIDDIMY)) # (x, y) tuple for grid start
            e = (np.random.randint(0, GRIDDIMX), np.random.randint(0, GRIDDIMY)) # (x, y) tuple for grid end

            while (distance((s[0], s[1]), (e[0], e[1])) < (GRIDDIMY + GRIDDIMX) / 2):
                s = (int(np.random.randint(0, GRIDDIMX)), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid start
                e = (np.random.randint(0, GRIDDIMX), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid end

            self.start = s
            self.end = e

            # possible transitions
            transitions = ["up", "down", "left", "right", "upright", "upleft", "downleft", "downright"]

            #their corresponding track types
            track_types = ["vertical", "vertical", "horizontal", "horizontal", "upright", "upleft", "downleft", "downright"]
            def addtrack(grid = g, curri = s[0], currj = s[1], dir_to_prev = "", avoid_transitions = []):
                # path has reached the goal
                if curri == e[0] and currj == e[1]:
                    return True

                # setting up the start tile
                if curri == s[0] and currj == s[1] and not grid[curri][currj] is Tile:
                    tiletype = ""
                    nexti, nextj = s[0], s[1]
                    choice = np.random.randint(0, 2)
                    avoid = []
                    if s[0] < e[0] and s[1] < e[1]:
                        tiletype = "downright"
                        if ["down", "right"][choice] == "down":
                            avoid = ["left", "right"]
                            nextj += 1
                            dir_to_prev = "up"
                        else:
                            avoid = ["up", "down"]
                            nexti += 1
                            dir_to_prev = "left"

                    if s[0] <= e[0] and s[1] >= e[1]:
                        tiletype = "upright"
                        if ["up", "right"][choice] == "up":
                            avoid = ["left", "right"]
                            nextj -=1
                            dir_to_prev = "down"
                        else:
                            avoid = ["up", "down"]
                            nexti += 1
                            dir_to_prev = "left"

                    if s[0] >= e[0] and s[1] <= e[1]:
                        tiletype =  "downleft"
                        if ["down", "left"][choice] == "down":
                            avoid = ["left", "right"]
                            nextj += 1
                            dir_to_prev = "up"
                        else:
                            avoid = ["up", "down"]
                            nexti -= 1
                            dir_to_prev = "right"

                    if s[0] == e[0] and s[1] == e[1]:
                        tiletype =  "upleft"
                        if ["up", "left"][choice] == "up":
                            avoid = ["left", "right"]
                            nextj -= 1
                            dir_to_prev = "down"
                        else:
                            avoid = ["up", "down"]
                            nexti -= 1
                            dir_to_prev = "right"

                    grid[s[0]][s[1]] = Tile(s[0], s[1], tiletype)
                    return addtrack(grid, nexti, nextj, dir_to_prev, avoid)

                #allow any transition
                this_transition = transitions.copy()
                this_track_type = track_types.copy()
                # allow 90% of the time a transition that will go closer to the goal
                if np.random.randint(0, 10) >= 0:
                    if not (s[0] == e[0] or s[1] == e[1]):
                        this_track_type = []

                        if s[0] < e[0] and s[1] < e[1]:
                            this_transition = ["down", "right", "downright"]
                        if s[0] < e[0] and s[1] > e[1]:
                            this_transition = ["up", "right", "upright"]
                        if s[0] > e[0] and s[1] < e[1]:
                            this_transition = ["down", "left", "downleft"]
                        if s[0] > e[0] and s[1] > e[1]:
                            this_transition = ["up", "left", "upleft"]

                        for transit in this_transition:
                            i = transitions.index(transit)
                            this_track_type.append(track_types[i])

                # remove the backtrack transition
                if dir_to_prev in this_transition:
                    this_track_type.pop(this_transition.index(dir_to_prev))
                    this_transition.pop(this_transition.index(dir_to_prev))

                remove_index = []
                # prevent going off the map
                for tr in range(0, len(this_transition)):

                    if (("right" in this_transition[tr] and curri + 1 >= GRIDDIMX) or
                        ("left" in this_transition[tr] and curri - 1 < 0) or
                         ("up" in this_transition[tr] and currj - 1 < 0) or
                          ("down" in this_transition[tr] and currj + 1 >= GRIDDIMY)):
                        remove_index.append(tr)

                for a in list(reversed(remove_index)):
                    this_track_type.pop(a)
                    this_transition.pop(a)

                avoid = []
                if dir_to_prev == "left" or dir_to_prev == "right":
                    avoid = ["up", "down"]
                elif dir_to_prev == "up" or dir_to_prev == "down":
                    avoid = ["left", "right"]
                #remove the transitions needed to be avoided (perpendicular)
                for transit in avoid:
                    if transit in this_transition:
                        i = this_transition.index(transit)
                        this_track_type.pop(i)
                        this_transition.pop(i)


                # if no transitions left... exit and try again
                if len(this_transition) == 0:
                    return False

                randtransition = np.random.randint(0, len(this_transition))
                grid[curri][currj] = Tile(curri, currj, this_track_type[randtransition])

                nexti, nextj = curri, currj
                previous = ""
                #where next tile will be
                avoid = []
                if "up" == this_transition[randtransition]:
                    nextj -= 1
                    previous = "down"
                    avoid = ["left", "right"]
                elif "down" == this_transition[randtransition]:
                    nextj += 1
                    previous = "up"
                    avoid = ["left", "right"]
                elif "left" == this_transition[randtransition]:
                    nexti -= 1
                    previous = "right"
                    avoid = ["up", "down"]
                elif "right" == this_transition[randtransition]:
                    nexti += 1
                    previous = "left"
                    avoid = ["up", "down"]
                else:
                    if "upright" == this_transition[randtransition]:
                        if dir_to_prev == "up": # coming from up, move right
                            nexti += 1
                            previous = "left"
                            avoid = ["up", "down"]
                        if dir_to_prev == "right": #coming from right, move up
                            nextj -= 1
                            previous = "down"
                            avoid = ["left", "right"]

                    if "downright" == this_transition[randtransition]:
                        if dir_to_prev == "down": # coming from down, move right
                            nexti += 1
                            previous = "left"
                            avoid = ["up", "down"]
                        if dir_to_prev == "right": #coming from right, move down
                            nextj += 1
                            previous = "up"
                            avoid = ["left", "right"]

                    if "upleft" == this_transition[randtransition]:
                        if dir_to_prev == "up": # coming from up, move left
                            nexti -= 1
                            previous = "right"
                            avoid = ["up", "down"]
                        if dir_to_prev == "left": #coming from left, move up
                            nextj -= 1
                            previous = "down"
                            avoid = ["left", "right"]

                    if "downleft" == this_transition[randtransition]:
                        if dir_to_prev == "down": # coming from down, move left
                            nexti -= 1
                            previous = "right"
                            avoid = ["up", "down"]
                        if dir_to_prev == "left": #coming from left, move down
                            nextj += 1
                            previous = "up"
                            avoid = ["left", "right"]


                if grid[nexti][nextj] is Tile:
                    return False

                return addtrack(grid, nexti, nextj, previous, avoid)

            # keep trying grid until it works
            is_success = addtrack()
            while not is_success:
                is_success = addtrack()


            # any empty tiles will become filled
            for col in range(0, GRIDDIMX):
                for row in range(0, GRIDDIMY):
                    if g[col][row] is None:
                        g[col][row] = Tile(col, row, "filled")

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