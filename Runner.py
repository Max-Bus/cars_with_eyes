from p5 import *
from population import Population
from mapdata import *
from racetrack import RaceTrack
from car import*
import time

r = RaceTrack()
p = Population(r, POPSIZE)
p.initialize_population()
FRAME_RATE = 30
MAX_TIME = FRAME_RATE*6
TIMER = 0

# c = Car(r.start[0], r.start[1], 0)

# first thing to run
def setup():
    size(SIMW, SIMH)


# runs immediately after setup
def draw():
    global TIMER
    no_stroke()
    background(50, 30, 190)

    r.display()
    if(TIMER < MAX_TIME):
        p.update(r.segment_translate(r.segments))
    else:
        p.next_gen()
        timer = 0

    remove = []
    for index, c in enumerate(p.cars):
        #print("car" + str(index) + "  " + str(c.x) + "   " + str(c.y))
        if c.collision():
            remove.append(index)

    for i in reversed(remove):
        p.cars.pop(i)

    TIMER+=1


def key_pressed(event):
    if event.key == 's':
        r.save_track()

    if event.key == 'l':
        r.load_track()
        time.sleep(3)
        p.reload(r)
        setup()



run(frame_rate=FRAME_RATE)

