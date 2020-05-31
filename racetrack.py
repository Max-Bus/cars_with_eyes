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

            while (distance((s[0], s[1]), (e[0], e[1])) < (GRIDDIMY + GRIDDIMX) / 2 - 2):
                s = (int(np.random.randint(0, GRIDDIMX)), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid start
                e = (np.random.randint(0, GRIDDIMX), np.random.randint(0, GRIDDIMY))  # (x, y) tuple for grid end

            self.start = s
            self.end = e
            # possible transitions
            transitions = ["up", "down", "left", "right", "upright", "upleft", "downleft", "downright"]

            #their corresponding track types
            track_types = ["vertical", "vertical", "horizontal", "horizontal", "upright", "upleft", "downleft", "downright"]

            #directions that should not be taken for the next track
            backtrack_directions = [["down"], ["up"], ["right"], ["left"], ["left", "down"], ["right", "down"], ["up", "right"], ["up", "left"]]
            def addtrack(grid = g, curri = s[0], currj = s[1], backwards = []):
                if curri == e[0] and currj == e[1]:
                    return True
                
                this_transition = transitions.copy()
                this_track_type = track_types.copy()
                this_bactrack_dirs = backtrack_directions.copy()


                # remove the backtrack transitions
                for trans in backwards:
                    this_track_type.pop(this_transition.index(trans))
                    this_bactrack_dirs.pop(this_transition.index(trans))
                    this_transition.pop(this_transition.index(trans))

                remove_index = []
                # prevent going off the map
                for tr in range(0, len(this_transition)):
                    print("up" in transitions[tr] and currj - 1 < 0)
                    if (("right" in transitions[tr] and curri + 1 >= GRIDDIMX) or
                        ("left" in transitions[tr] and curri - 1 < 0) or
                         ("up" in transitions[tr] and currj - 1 < 0) or
                          ("down" in transitions[tr] and currj + 1 >= GRIDDIMY)):
                        remove_index.append(tr)

                for a in list(reversed(remove_index)):
                    this_track_type.pop(a)
                    this_transition.pop(a)
                    this_bactrack_dirs.pop(a)


                # if no transitions left... exit and try again
                if len(this_transition) == 0:
                    return False

                print(currj)
                randtransition = np.random.randint(0, len(this_transition))
                g[curri][currj] = Tile(curri, currj, this_track_type[randtransition])

                nexti, nextj = (curri, currj)
                if this_transition[randtransition].__contains__("up"):
                    nextj -= 1
                elif this_transition[randtransition].__contains__("down"):
                    nextj += 1

                if this_transition[randtransition].__contains__("left"):
                    nexti -= 1
                elif this_transition[randtransition].__contains__("right"):
                    nexti += 1

                addtrack(g, nexti, nextj, this_bactrack_dirs[randtransition])
                    
            # keep trying grid until it works
            is_success = addtrack()
            while not is_success:
                is_success = addtrack()

            # any empty tiles will become filled
            for col in range(0, GRIDDIMX):
                for row in range(0, GRIDDIMY):
                    if g[col][row] is int:
                        g[col][row] = Tile(col, row, "filled")


            self.grid = g

        else:
            self.grid = grid
            self.end = end
            self.start = start


    def display(self):
        for col in self.grid:
            for tl in col:
                tl.show()