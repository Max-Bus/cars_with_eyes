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
