import numpy as np
from car import Car
from mapdata import *

class Population:


    def __init__(self, startx, starty, size):
        self.size = size

        initial_rotation = 0

        # topright
        if startx > SIMW / 2 and starty < SIMH / 2:
            initial_rotation = 225
        # topleft
        elif startx < SIMW / 2 and starty < SIMH / 2:
            initial_rotation = 315
        # bottomleft
        elif startx < SIMW / 2 and starty > SIMH / 2:
            initial_rotation = 45
        # bottomright
        elif startx > SIMW / 2 and starty > SIMH / 2:
            initial_rotation = 135

        self.cars = [Car(startx, starty, initial_rotation) for i in range(size)]

    def update(self,segments):
        for i in range(self.size):
            self.cars[i].update(segments)

