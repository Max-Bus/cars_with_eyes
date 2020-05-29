from p5 import *

class Car:

    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty

    def move(self, force):
        self.x += force.x
        self.y += force.y
