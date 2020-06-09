from p5 import *
from mapdata import*
class Car:

    def __init__(self, startx, starty,direction,neural_net):
        self.x = startx
        self.y = starty
        self.dir = direction
        self.width=5
        self.height=10
        self.speed=1
        self.feelers = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.feelerSlope = [0,22.5,45,90,135,180,225,270,315,337.5]
        self.neural_net = neural_net

    def update(self,segments,goal):
        self.move()
        self.feelers = self.see(segments)
        self.drawcar()
        self.jesus_take_the_wheel(goal)
    def move(self):
        changex = self.speed * cos(radians(self.dir))
        changey = self.speed * sin(radians(self.dir))
        self.x += changex
        self.y += changey
    def throttle(self,acceleration):
        self.speed+=acceleration
        if self.speed > 5:
            self.speed = 5
    def turn(self,degrees):
        if(degrees>45):
            degrees=45
        self.dir += degrees
        self.dir = self.dir%360
    def drawcar(self):
        with push_matrix():
            translate(self.x,self.y,0)
            rotate_z(radians(self.dir))
            fill(0,100,0)
            rect_mode(CENTER)
            rect((0, 0), self.height,self.width)
            '''
            for i in range(len(self.feelers)):
                stroke(0,100,0)
                if(self.feelers[i]==-1):
                    continue
                x1=self.feelers[i] * cos(radians(self.feelerSlope[i]))
                y1=self.feelers[i] * sin(radians(self.feelerSlope[i]))
                if(x1==0 and y1 ==0):
                    break
                line((0,0),(x1,y1))
            '''

    def see(self,lines):
        feelers = [-1]*len(self.feelers)
        for line in lines:
            for i in range(len(self.feelers)):
                p1 = line[0]
                p2= line[1]

                a1 = p2.y - p1.y
                b1 = p1.x - p2.x
                c1 = a1*p1.x+b1*p1.y

                absangle = (self.dir+self.feelerSlope[i]) % 360

                p3 = Point(self.x+cos(radians(absangle)),self.y+sin(radians(absangle)))

                a2 = p3.y - self.y
                b2 = self.x - p3.x
                c2 = a2*self.x+b2*self.y


                determinant = a1*b2- b1*a2
                if(determinant != 0):
                    x = (b2 * c1 - b1 * c2) / determinant
                    y = (a1 * c2 - a2 * c1) / determinant
                    bottomx = min(p1.x,p2.x)
                    topx = max(p1.x,p2.x)
                    bottomy = min(p2.y,p1.y)
                    topy = max(p2.y, p1.y)

                    if((p3.x < self.x and x > self.x) or (p3.x > self.x and x < self.x)):
                        continue

                    if ((p3.y < self.y and y > self.y) or (p3.y > self.y and y < self.y)):
                        continue

                    if(bottomx <= x <= topx and bottomy <= y <= topy):
                        far = distance((self.x, self.y), (x, y))
                        if(feelers[i]==-1 or far < feelers[i]):
                            feelers[i] = far

                else:
                    feelers[i]=-1
        return feelers

    def collision(self):
        if(self.x < 0 or self.x > SIMW):
            return True

        if (self.y < 0 or self.y > SIMW):
            return True



        p1 = Point(self.x + self.width / 2, self.y + self.height / 2)
        p2 = Point(self.x - self.width / 2, self.y + self.height / 2)
        p3 = Point(self.x - self.width / 2, self.y - self.height / 2)
        p4 = Point(self.x + self.width / 2, self.y - self.height / 2)
        points = [p1,p2,p3,p4]
        mysegments=[]
        for n in range(4):
            for i in range(n+1,4):
                mysegments.append([points[n],points[i]])
        borders = self.see(mysegments)
        for i in range(len(self.feelers)):
            if(borders[i]+3 > self.feelers[i] and self.feelers[i] != -1):
                return True



        return False

        # in the absence of a better idea

    def jesus_take_the_wheel(self,goal):
        # make the car be able to see in 8 directions record distance
        # get speed and direction
        # feed these numbers into nueral net
        # take the output of the neural net
        # inputs = 10 feelers, speed, direction, x, y
        inputs = self.feelers.copy()
        inputs.append(self.speed)
        inputs.append(self.dir)
        inputs.append(goal.x-self.x)
        inputs.append(goal.y-self.y)

        neural_net_output = self.neural_net.answer_to_everything(inputs)
        self.turn(neural_net_output[0]*10)
        self.throttle(neural_net_output[1])

