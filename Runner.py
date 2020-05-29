from p5 import *

SIMH = 900
SIMW = 1000

# first thing to run
def setup():
    size(SIMW, SIMH)
    background(200)

# runs immediately after setup
def draw():
    print("hello")


run()

