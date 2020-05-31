from p5 import *
from population import Population
from mapdata import *
from racetrack import RaceTrack

p = Population(0, 0, POPSIZE)

# first thing to run
def setup():
    size(SIMW, SIMH)
    r = RaceTrack()
    r.display()

# runs immediately after setup
def draw():
    no_stroke()
    rect_mode("CENTER")
    background(200)
    # draw the track

    # for car in p.cars:
      #   fill(np.random.uniform(0, 255), np.random.uniform(0, 255), np.random.uniform(0, 255), 30)
      #   rect((car.x, car.y), 30, 40)
      #   car.move(Vector(np.random.uniform(-3, 3), np.random.uniform(-3, 3)))


run(frame_rate=30)

