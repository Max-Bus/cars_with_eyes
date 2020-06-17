from p5 import *
from population import Population
from mapdata import *
from racetrack import RaceTrack
from car import*
import time

r = RaceTrack()
p = Population(r, 1)
p.initialize_population("general_9",None)
FRAME_RATE = 30
MAX_TIME = 20*FRAME_RATE
TIMER = 0
MAXGEN = 15
TIME_CHANGE = False

# c = Car(r.start[0], r.start[1], 0)

# first thing to run
def setup():
    size(SIMW, SIMH)


# runs immediately after setup
def draw():
    global TIMER
    global MAX_TIME
    global MAXGEN
    global TIME_CHANGE
    no_stroke()
    background(90, 230, 130)

    r.display()
    if(TIMER < MAX_TIME and len(p.cars)>0):
        p.update(r.segment_translate(r.segments),True,True)
    else:
        if (MAXGEN == 0):
            p.cars.sort(reverse=True, key=p.fitness)
            if p.cars[0].won:
                p.save_car(p.cars[0], "good_tester_solver")
                exit()
            else:
                MAX_TIME += 1
                MAXGEN=1
        if (len(p.cars)>0):
            p.cars.sort(reverse=True, key=p.fitness)
            if(len(p.cars)>0.5*p.size and (not p.cars[0].won) and (not TIME_CHANGE)):
                if (not MAX_TIME >= FRAME_RATE*30):
                    MAX_TIME += FRAME_RATE*2
                    print(MAX_TIME/FRAME_RATE)
            if p.cars[0].won:
                print("new PB")
                MAX_TIME = min(p.cars[0].time_alive,MAX_TIME)
                if MAX_TIME == p.cars[0].time_alive:
                    print("a car won its time was:"+str(MAX_TIME / FRAME_RATE))
                    TIME_CHANGE =True
        p.next_gen(True)
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
        p.initialize_population("good_tester_solver",None)
        setup()


run(frame_rate=FRAME_RATE)


