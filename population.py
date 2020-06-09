import numpy as np
from car import Car
from mapdata import *
from neural_net import *
from p5 import *

class Population:


    def __init__(self, racetrack, size):
        self.size = size
        self.innovation = 0
        startx = racetrack.start.x
        starty = racetrack.start.y
        self.goal = Point(racetrack.end.x,racetrack.end.y)

        initial_rotation = 0

        # topright
        if startx > SIMW / 2 and starty < SIMH / 2:
            initial_rotation = 135
        # topleft
        elif startx < SIMW / 2 and starty < SIMH / 2:
            initial_rotation = 45
        # bottomleft
        elif startx < SIMW / 2 and starty > SIMH / 2:
            initial_rotation = 315
        # bottomright
        elif startx > SIMW / 2 and starty > SIMH / 2:
            initial_rotation = 225

        self.cars = [Car(startx, starty, initial_rotation,None) for i in range(size)]

    def next_gen(self):
        species = self.speciate()


    def speciate(self):
        species = []
        speciated = []
        num_species = 0
        for i in range(len(self.cars)):
            if(i in speciated):
                continue
            species.append([])
            for j in range(i,len(self.cars)):
                if self.cars[i].neural_net.compareNets(self.cars[i].neural_net):
                    species[num_species].append(self.cars[i])
                    speciated.append(j)
            num_species+=1



    def update(self,segments):
        for c in self.cars:
            c.update(segments)


    def reload(self, racetrack):
        startx = racetrack.start.x
        starty = racetrack.start.y

        initial_rotation = 0

        # topright
        if startx > SIMW / 2 and starty < SIMH / 2:
            initial_rotation = 135
        # topleft
        elif startx < SIMW / 2 and starty < SIMH / 2:
            initial_rotation = 45
        # bottomleft
        elif startx < SIMW / 2 and starty > SIMH / 2:
            initial_rotation = 315
        # bottomright
        elif startx > SIMW / 2 and starty > SIMH / 2:
            initial_rotation = 225

        self.cars = [Car(startx, starty, initial_rotation, None) for i in range(self.size)]

    def fitness(self,car):
        far = distance((car.x,car.y),self.goal)
        if far<=10:
            return 10000

        return -1*far

    def initialize_population(self):
        inputs = 14
        outputs = 2

        for c in self.cars:
            genome = []
            for outs in range(outputs):
                for ins in range(inputs):
                    self.innovation+=1
                    genome.append(NodeConnection(outs * inputs + ins, "in_" + str(ins), "out_" + str(outs), np.random.randn(), np.random.randn()))

            c.neural_net = NeuralNet(genome)

        self.cars[0].neural_net.print_net()


class NodeConnection:
    def __init__(self,innovation, in_ID, out_ID, weight, out_bias):
        self.innovation = innovation
        self.out_bias = out_bias
        self.in_ID = in_ID
        self.out_ID = out_ID
        self.weight = weight