from p5 import *
from mapdata import*
class Car:

    def __init__(self, startx, starty,direction):
        self.x = startx
        self.y = starty
        self.dir = direction
        self.width=5
        self.height=10
        self.speed=0
        self.feelers = [0,0,0,0,0,0,0,0]
        self.feelerSlope = [0,45,90,135,180,225,270,315]

    def update(self):
        self.move()
        self.drawcar()
    def move(self):
        changex = self.speed * cos(radians(self.dir))
        changey = self.speed * sin(radians(self.dir))
        self.x += changex
        self.y += changey
    def throttle(self,acceleration):
        self.speed+=acceleration
    def turn(self,degrees):
        if(degrees>45):
            degrees=45
        self.dir += degrees
        self.dir = self.dir%360
    def drawcar(self):
        push_matrix()
        translate(self.x,self.y,0)
        rotate_z(self.dir)
        fill(0,100,0)
        rect_mode(CENTER)
        rect((0, 0), self.height,self.width)
        for i in range(len(self.feelers)):
            stroke(0,100,0)
            x1=self.feelers[i] * cos(radians(self.feelerSlope[i]))
            y1=self.feelers[i] * sin(radians(self.feelerSlope[i]))
            if(x1==0 and y1 ==0):
                break
            line((0,0),(x1,y1))
        pop_matrix()

    def see(self,lines):

        for line in lines:
            for i in range(0,8):
                p1 = line[0]
                p2= line[1]
                if(p1.x != p2.x):
                    slope = (p1.y-p2.y)/(p1.x-p2.x)
                    yint = slope * (-1 * p1.x) + p1.y
                    angle = self.feelerSlope[i]
                    myslope = tan(radians(angle))
                    myyint = myslope * (-1 * self.x) + self.y
                    if(myslope==slope):
                        break

                    interceptx = (yint-myyint)/(myslope-slope)
                    intercepty = myslope*interceptx+self.y

                    bottom = min(p1.x,p2.x)
                    top = max(p1.x,p2.x)
                    if not(interceptx in range(min,max)):
                        break
                    distance = dist(self.x,self.y,interceptx,intercepty)

                    self.feelers[i]= min(distance,self.feelers[i])

                else:
                    if(cos(radians(self.feelerSlope[i]+self.dir)) == 0):
                        break
                    else:
                        dx = p1.x - self.x
                        angle=self.feelerSlope[i]
                        slope = tan(radians(angle))
                        dy = slope * dx
                        distance=sqrt(dx*dx+dy*dy)
                        if(distance<self.feelers[i]):
                            self.feelers=distance

    def collision(self):
        diagnal = sqrt(self.width*self.width+self.height*self.height)
        if (self.feelers[0] < self.width/2):
            return True
        if (self.feelers[1] < diagnal):
            return True
        if (self.feelers[2] < self.height/2):
            return True
        if (self.feelers[3] < diagnal):
            return True
        if (self.feelers[4] < self.width/2):
            return True
        if (self.feelers[5] < diagnal):
            return True
        if (self.feelers[6] < self.height/2):
            return True
        if (self.feelers[7] < diagnal):
            return True


        # in the absence of a better idea

    def jesus_take_the_wheel(self):
        # make the car be able to see in 8 directions record distance
        # get speed and direction
        # feed these numbers into nueral net
        # take the output of the neural net
        neural_net_output=0
        self.turn(neural_net_output)
        self.throttle(neural_net_output)

