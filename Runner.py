from p5 import *
from population import Population
from mapdata import *
from racetrack import RaceTrack
from car import*
import time

r = RaceTrack()
p = Population(r.start[0], r.start[1], POPSIZE)
c = Car(r.start[0], r.start[1], 0)

# first thing to run
def setup():
    size(SIMW, SIMH)

# runs immediately after setup
def draw():
    no_stroke()
    r.display()
    p.update(r.segment_translate(r.segments))


def key_pressed(event):
    if event.key == 's':
        r.save_track()

    if event.key == 'l':
        r.load_track()
        time.sleep(2.5)
        redraw()


run(frame_rate=30)

