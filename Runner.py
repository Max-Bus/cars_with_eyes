from p5 import *
from population import Population
from mapdata import *
from racetrack import RaceTrack
from car import*
import time

r = RaceTrack()
p = Population(r, POPSIZE)
p.initialize_population(None)
FRAME_RATE = 30
MAX_TIME = 3*FRAME_RATE
TIMER = 0
MAXGEN = 1000

# c = Car(r.start[0], r.start[1], 0)

# first thing to run
def setup():
    size(SIMW, SIMH)


# runs immediately after setup
def draw():
    global TIMER
    global MAX_TIME
    global MAXGEN
    if(MAXGEN==0):
        p.cars.sort(reverse=True, key=p.fitness)
        p.save_car(p.cars[0],"first_batch")
        exit()
    no_stroke()
    background(90, 230, 130)

    r.display()
    if(TIMER < MAX_TIME and len(p.cars)>0):
        p.update(r.segment_translate(r.segments),TIMER%2==0)
    else:
        if(len(p.cars)>0.5*p.size):
            p.cars.sort(reverse=True, key = p.fitness)
            if not MAX_TIME == FRAME_RATE*30 and not p.cars[0].won:
                MAX_TIME += FRAME_RATE*2
                print(MAX_TIME/FRAME_RATE)
            elif p.cars[0].won:
                MAX_TIME = p.cars[0].time_alive
        p.next_gen()
        MAXGEN-=1
        TIMER = 0

    remove = []
    for index, c in enumerate(p.cars):
        #print("car" + str(index) + "  " + str(c.x) + "   " + str(c.y))
        if c.collision():
            remove.append(index)

    for i in reversed(remove):
        removed_car = p.cars.pop(i)
        removed_car.is_crashed = True
        p.crashed_cars.append(removed_car)

    TIMER+=1


def key_pressed(event):
    if event.key == 's':
        r.save_track()

    if event.key == 'l':
        global p
        r.load_track()
        time.sleep(3)
        p = Population(r, POPSIZE)
        p.initialize_population(None)
        setup()


run(frame_rate=FRAME_RATE)


