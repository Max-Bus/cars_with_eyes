from tile import Tile
import numpy as np
from p5 import *
from mapdata import *
import os

class RaceTrack:

    def __init__(self):
        num_xtiles = PTCOUNT
        tilewidth = SIMW / num_xtiles
        trackwidth = SIMW / 5

        start_pos = ["topleft", "topright", "bottomleft", "bottomright"][np.random.randint(0, 4)]

        s = None # starting point
        e = None # goal point

        # generate the x points for the track
        xvals = [np.random.randint(tilewidth * x, tilewidth * (x + 1)) for x in range(1, num_xtiles - 1)]

        slope = [] # will store a range of the slope to get the y values

        segment_list = []  # stores a list of lists containing the 4 vertices of each segment
        # s.x > e.x and s.y < e.y


        # s.x < e.x and s.y < e.y
        if start_pos == "topleft":
            s = Point(trackwidth / 2, trackwidth / 2)
            e = Point(SIMW - trackwidth / 2, SIMH - trackwidth / 2)

            slope = [-0.5, 1.5]
            for i in range(len(slope)):
                slope[i] *= 0.20
            dy = 0.20
            curr_segment = [Point(0, 0), Point(0, trackwidth)]

            currx = 0
            curry = 0
            for segment in range(0, num_xtiles - 1):
                if segment == num_xtiles - 2:
                    segment_list.append(curr_segment)
                    continue

                curry = curry + dy * (xvals[segment] - currx)
                currx = xvals[segment]

                vshift = np.random.uniform(-tilewidth, tilewidth)
                if curry + vshift > tilewidth and curry + vshift < SIMH - tilewidth:
                    curry += 0.35 * vshift

                next1 = Point(currx, curry)
                next2 = Point(currx, curry + (np.random.uniform(0.7, 1.1)) * trackwidth)
                curr_segment.append(next2)
                curr_segment.append(next1)

                if len(curr_segment) == 4:
                    segment_list.append(curr_segment)
                    curr_segment = [next1, next2]

                acc = 0.10 * math.cos(np.random.uniform(0, math.pi)) + 1.0 / (distance((currx, curry), (e.x, e.y)) ) + 0.0002 * distance((currx, curry), (e.x, e.y))
                if np.random.randint(0, 5) == 0:
                    acc -= np.random.uniform(0,  0.1)
                dy += acc

            segment_list[num_xtiles - 2].append(Point(SIMW, SIMH))
            segment_list[num_xtiles - 2].append(Point(SIMW, SIMH - trackwidth))




        elif start_pos == "topright":
            s = Point(SIMW - trackwidth / 2, trackwidth / 2)
            e = Point(trackwidth / 2, SIMH - trackwidth / 2)

            slope = [-1.5, 0.5]
            for i in range(len(slope)):
                slope[i] *= 0.20
            # reverse because we are going from right to left here
            xvals = list(reversed(xvals))
            dy = -0.20
            curr_segment = [Point(SIMW, 0), Point(SIMW, trackwidth)]

            currx = SIMW
            curry = 0
            for segment in range(0, num_xtiles - 1):
                if segment == num_xtiles - 2:
                    segment_list.append(curr_segment)
                    continue


                curry = curry + dy * (xvals[segment] - currx)
                currx = xvals[segment]

                vshift = np.random.uniform(-tilewidth, tilewidth)
                if curry + vshift > tilewidth and curry + vshift < SIMH - tilewidth:
                    curry += 0.35 * vshift

                next1 = Point(currx, curry)
                next2 = Point(currx, curry + (np.random.uniform(0.7, 1.1)) * trackwidth)
                curr_segment.append(next2)
                curr_segment.append(next1)

                if len(curr_segment) == 4:
                    segment_list.append(curr_segment)
                    curr_segment = [next1, next2]

                acc = 0.10 * math.cos(np.random.uniform(0, math.pi)) + 1.0 / (distance((currx, curry), (e.x, e.y)) ) + 0.0002 * distance((currx, curry), (e.x, e.y))
                if np.random.randint(0, 5) == 0:
                    acc += np.random.uniform(- 0.1, 0)

                dy -= acc


            segment_list[num_xtiles - 2].append(Point(0, SIMH))
            segment_list[num_xtiles - 2].append(Point(0, SIMH - trackwidth))


        # s.x < e.x and s.y > e.y
        elif start_pos == "bottomleft":
            s = Point(trackwidth / 2, SIMH - trackwidth / 2)
            e = Point(SIMW - trackwidth / 2, trackwidth / 2)

            slope = [-1.5, 0.5]
            for i in range(len(slope)):
                slope[i] *= 0.20
            dy = -0.20
            curr_segment = [Point(0, SIMH - trackwidth), Point(0, SIMH)]

            currx = 0
            curry = SIMH - trackwidth
            for segment in range(0, num_xtiles - 1):
                if segment == num_xtiles - 2:
                    segment_list.append(curr_segment)
                    continue

                curry = curry + dy * (xvals[segment] - currx)
                currx = xvals[segment]

                vshift = np.random.uniform(-tilewidth, tilewidth)
                if curry + vshift > tilewidth and curry + vshift < SIMH - tilewidth:
                    curry += 0.35 * vshift

                next1 = Point(currx, curry)
                next2 = Point(currx, curry + (np.random.uniform(0.7, 1.1)) * trackwidth)
                curr_segment.append(next2)
                curr_segment.append(next1)

                if len(curr_segment) == 4:
                    segment_list.append(curr_segment)
                    curr_segment = [next1, next2]

                acc = 0.10 * math.cos(np.random.uniform(0, math.pi)) + 1.0 / (distance((currx, curry), (e.x, e.y)) ) + 0.0002 * distance((currx, curry), (e.x, e.y))
                if np.random.randint(0, 5) == 0:
                    acc += (np.random.uniform(- 0.1, 0))
                dy -= acc

            segment_list[num_xtiles - 2].append(Point(SIMW, trackwidth))
            segment_list[num_xtiles - 2].append(Point(SIMW, 0))



        # s.x > e.x and s.y > e.y
        else:
            s = Point(SIMW - trackwidth / 2, SIMH - trackwidth / 2)
            e = Point(trackwidth / 2, trackwidth / 2)

            slope = [-0.5, 1.5]
            for i in range(len(slope)):
                slope[i] *= 0.20

            # reverse because we are going from right to left here
            xvals = list(reversed(xvals))
            dy = 0.20
            curr_segment = [Point(SIMW, SIMH - trackwidth), Point(SIMW, SIMH)]

            currx = SIMW
            curry = SIMH - trackwidth
            for segment in range(0, num_xtiles - 1):
                if segment == num_xtiles - 2:
                    segment_list.append(curr_segment)
                    continue

                curry = curry + dy * (xvals[segment] - currx)
                currx = xvals[segment]

                vshift = np.random.uniform(-tilewidth, tilewidth)
                if curry + vshift > tilewidth and curry + vshift < SIMH - tilewidth:
                    curry += 0.35 * vshift

                next1 = Point(currx, curry)
                next2 = Point(currx, curry + (np.random.uniform(0.7, 1.1)) * trackwidth)
                curr_segment.append(next2)
                curr_segment.append(next1)

                if len(curr_segment) == 4:
                    segment_list.append(curr_segment)
                    curr_segment = [next1, next2]

                acc = 0.10 * math.cos(np.random.uniform(0, math.pi)) + 1.0 / (distance((currx, curry), (e.x, e.y)) ) + 0.0002 * distance((currx, curry), (e.x, e.y))
                if np.random.randint(0, 5) == 0:
                    acc -= np.random.uniform(0, 0.1)
                dy += acc

            segment_list[num_xtiles - 2].append(Point(0, trackwidth))
            segment_list[num_xtiles - 2].append(Point(0, 0))


        self.start = Point((segment_list[0][0].x + segment_list[0][1].x) / 2, (segment_list[0][0].y + segment_list[0][1].y) / 2)
        self.end = Point((segment_list[len(segment_list) - 1][3].x + segment_list[len(segment_list) - 1][2].x) / 2, (segment_list[len(segment_list) - 1][3].y + segment_list[len(segment_list) - 1][2].y) / 2)
        self.segments = segment_list

        self.checkpoints = []
        self.checkpoint_maker()

        self.segments_for_car = self.segment_translate(self.segments)

    def segment_translate(self, segments):
        car_segs = []
        for quads in segments:
            car_segs.append([quads[0],quads[3]])
            car_segs.append([quads[1],quads[2]])

        return car_segs
    def save_track(self):
        name = input("Save as... (.txt will be added) ")
        while os.path.exists("tracks/" + name + ".txt"):
            name = input("This name is taken. Save as... ")

        file = open("tracks/" + name + ".txt", "w")
        file.write(str(self.start.x) + "|" + str(self.start.y))
        file.write("\n" + str(self.end.x) + "|" + str(self.end.y) + "\n")
        for segment in self.segments:
            for point in segment:
                file.write(str(point.x)+","+str(point.y)+"|")
            file.write("\n")
        file.close()
        print("save")

    def load_track(self):
        name = input("Load... (.txt will be added) ")
        while not os.path.exists("tracks/" + name + ".txt"):
            name = input("This file does not exist. Load.... ")

        with open("tracks/" + name + ".txt", "r") as file:
            allines = file.readlines()
            st = allines[0].strip().split("|")
            en = allines[1].strip().split("|")
            self.start = Point(float(st[0]), float(st[1]))
            self.end = Point(float(en[0]), float(en[1]))

            new_segments = []
            for line in allines[2:]:
                line.strip()
                points = line.split("|")
                new_segments.append([])
                for point in points:
                    if point == "\n":
                        break
                    point.strip()
                    vals = point.split(",")
                    x = float(vals[0])
                    y = float(vals[1])
                    p = Point(x,y)
                    new_segments[len(new_segments)-1].append(p)
            self.segments= new_segments
        self.checkpoint_maker()
        self.segments_for_car = self.segment_translate(self.segments)
        print("loaded")
        clear()
        self.display()
    def checkpoint_maker(self):
        self.checkpoints.clear()
        for section in self.segments:
            avg2 = (section[2].y + section[3].y) / 2
            second_checkpoint = Point(section[2].x, avg2)
            self.checkpoints.append(second_checkpoint)
    def display(self):
        rect_mode('CENTER')

        fill(145, 132, 134)
        for seg in self.segments:
            begin_shape()
            for pt in seg:
                vertex(pt.x, pt.y)
            end_shape()

        fill(219, 127, 144)
        rect((self.start.x, self.start.y), 40, 100)

        fill(55, 214, 0)
        ellipse((self.end.x, self.end.y), 40, 40)

        fill('black')


    """
    def __init__(self, grid=None, start=None, end=None, dimx=GRIDDIMX, dimy=GRIDDIMY):
        if (grid == None or start == None or end == None):
            self.dimx = dimx
            self.dimy = dimy

            g = [[None for y in range(dimy)] for x in range(dimx)]  # null grid
            s = (int(np.random.randint(0, dimx)), np.random.randint(0, dimy))  # (x, y) tuple for grid start
            e = (np.random.randint(0, dimx), np.random.randint(0, dimy))  # (x, y) tuple for grid end

            # repick start and end if too close to each other
            while (distance((s[0], s[1]), (e[0], e[1])) < (dimy + dimx) / 2):
                s = (int(np.random.randint(0, dimx)), np.random.randint(0, dimy))  # (x, y) tuple for grid start
                e = (np.random.randint(0, dimx), np.random.randint(0, dimy))  # (x, y) tuple for grid end

            self.start = s
            self.end = e

            # possible transitions
            transitions = ["up", "down", "left", "right"]
            def addtrack(track=None, currx=s[0], curry=s[1], dir_to_prev=""):
                if track is None:
                    track = g

                allowed_transitions = []
                # limit to directions that tend towards the goal (remove these and branching will be reintroduced)
                if s[0] < e[0]:
                    allowed_transitions.append("right")
                elif s[0] > e[0]:
                    allowed_transitions.append("left")

                if s[1] < e[1]:
                    allowed_transitions.append("down")
                elif s[1] > e[1]:
                    allowed_transitions.append("up")

                if s[0] == e[0]:
                    if s[1] < e[1] and "down" not in allowed_transitions:
                        allowed_transitions.append("down")
                    elif s[1] > e[1] and "up" not in allowed_transitions:
                        allowed_transitions.append("up")

                if s[1] == e[1]:
                    if s[0] < e[0] and "right" not in allowed_transitions:
                        allowed_transitions.append("right")
                    elif s[0] > e[0] and "left" not in allowed_transitions:
                        allowed_transitions.append("left")


                # remove transitions that will go off the screen
                if currx == 0 and "left" in allowed_transitions:
                    allowed_transitions.remove("left")
                if currx == dimx - 1 and "right" in allowed_transitions:
                    allowed_transitions.remove("right")
                if curry == 0 and "up" in allowed_transitions:
                    allowed_transitions.remove("up")
                if curry == dimy - 1 and "down" in allowed_transitions:
                    allowed_transitions.remove("down")

                # remove the previously visited tile to avoid backtracking
                if dir_to_prev in allowed_transitions:
                    allowed_transitions.remove(dir_to_prev)

                    # path has reached the goal
                if currx == e[0] and curry == e[1]:
                    return True

                elif (len(allowed_transitions) == 0):
                    return False

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



                return addtrack(track, nextx, nexty, to_previous)

            # keep trying grid until it works
            is_success = addtrack(track=g)
            while not is_success:
                g = [[None for y in range(dimy)] for x in range(dimx)]
                is_success = addtrack(track=g)

            # any empty tiles will become filled
            for col in range(0, dimx):
                for row in range(0, dimy):
                    if g[col][row] is None:
                        g[col][row] = Tile(col, row, "filled")


            g[s[0]][s[1]].is_start = True
            g[s[0]][s[1]].type = "start"
            g[e[0]][e[1]].is_goal = True
            g[e[0]][e[1]].type = "end"
            self.grid = g

        else:
            self.grid = grid
            self.end = end
            self.start = start
            self.dimx = dimx
            self.dimy = dimy

    def display(self):
        for col in self.grid:
            for tl in col:
                tl.show()

    def save_track(self):
        if self.dimy * self.dimx > 100:
            print("GRID TOO LARGE; MAX 100 TILES")
            return

        name = input("Save as... (.txt will be added) ")
        while os.path.exists("tracks/" + name + ".txt"):
            name = input("This name is taken. Save as... ")

        file = open("tracks/" + name + ".txt", "w")

        file.write("x:" + str(self.dimx) + "\n")
        file.write("y:" + str(self.dimy) + "\n")
        m = np.matrix(self.grid).transpose().A1.tolist()
        for x, t in enumerate(m):
            if (x % self.dimx == 0 and x != 0):
                file.write("\n")
            file.write(t.get_type_for_file() + " ")

        #for x in range(0, len(self.grid)):
         #   for y in range(0, len(self.grid[x])):

          #      file.write(np.matrix(t.get_type_for_file() + " "))

           # file.write("\n")

        file.close()
        print("Saved")


    def load_track(self):
        name = input("Load... (.txt will be added) ")
        while not os.path.exists("tracks/" + name + ".txt"):
            name = input("This file does not exist. Load.... ")

        xlen = 0
        ylen = 0
        lgrid = []
        st = () # start
        en = () # end
        with open("tracks/" + name + ".txt", "r") as file:
            lines = file.readlines()
            xlen = int(lines[0][lines[0].index(":") + 1].strip())
            ylen = int(lines[1][lines[1].index(":") + 1].strip())

            lgrid = [[None for x in range(xlen)] for y in range(ylen)]
            for y, line in enumerate(lines[2:]):
                for x, ttype in enumerate(line.strip().split(" ")):
                    if ttype == "s":
                        st = (x, y)
                    if ttype == "e":
                        en = (x, y)

                    lgrid[x][y] = Tile(x, y, Tile.get_type_from_file(ttype), xlen, ylen)

        lgrid[st[0]][st[1]].is_start = True
        lgrid[en[0]][en[1]].is_goal = True

        self.grid = lgrid
        self.start = st
        self.end = en
        self.dimx = xlen
        self.dimy = ylen

        print("loaded")
    """
