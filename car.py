from p5 import *

class Car:

    def __init__(self, startx, starty,direction):
        self.x = startx
        self.y = starty
        self.dir = direction
        self.width=5
        self.height=10
        self.speed=0
        self.feelers = []

    def move(self, force):
        changex = self.speed * cos(radians(self.dir))
        changey = self.speed * sin(radians(self.dir))
        self.x += changex
        self.y += changey
    def throttle(self,acceleration):
        self.speed+=acceleration
    def turn(self,degrees):
        self.dir += degrees
        self.dir%=360
    def drawcar(self):
        push_matrix()
        rotate_z(radians(self.dir))
        rect(self.x-self.width/2.0,self.y-self.height/2.0)
        pop_matrix()

    def see(self, ):
        # in the absence of a better idea

    def jesus_take_the_wheel(self):
        # make the car be able to see in 8 directions record distance
        # get speed and direction
        # feed these numbers into nueral net
        # take the output of the neural net
        neural_net_output=0
        self.turn(neural_net_output)
        self.throttle(neural_net_output)

