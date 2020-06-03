from p5 import *
from population import Population
from mapdata import *
from racetrack import RaceTrack
import time


# p = Population(0, 0, POPSIZE)
r = RaceTrack()

# first thing to run
def setup():
    size(SIMW, SIMH)

# runs immediately after setup
def draw():
    no_stroke()
    r.display()

def key_pressed(event):
    if event.key == 's':
        r.save_track()

    if event.key == 'l':
        r.load_track()
        time.sleep(2.5)
        redraw()


run(frame_rate=30)

