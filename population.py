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


    def crossover(self, car1, car2):
        # car1 more fit

        genome1 = car1.neural_net.genome
        genome2 = car2.neural_net.genome

        genome1.sort(reverse=False, key=self.connectionSort)
        genome2.sort(reverse=False, key=self.connectionSort)

        # in both (randomly choose from 1 if gene is common between the two)
        # disjoint = not in other car (all disjoints passed down)
        # excess : from longer genome (larger innov num than other car) (excess passed from fitter car)

        new_genome = []
        excess = []
        max_innov_genome1 = 0
        max_innov_genome2 = 0
        for i, j in range(len(genome1)), range(len(genome2)):
            max_innov_genome1 += 1
            max_innov_genome2 += 1


            # overlap
            if genome1[i].innovation == genome2[j].innovation:
                if np.random.randint(0, 2) == 0:
                    new_genome.append(new_genome[i])
                else:
                    new_genome.append(genome2[j])

            # disjoint
            elif genome1[i].innovation != genome2[j].innovation:
                if genome1[i].innovation < genome2[j].innovation:
                    new_genome.append(genome1[i])
                    j -= 1

                else:
                    new_genome.append(genome1[j])
                    i -= 1

            # car1 genome is longer
            if j == len(genome2):
                excess = genome1[i:]

        new_genome += excess
        return new_genome



    def connectionSort(self,connection):
        return connection.innovation


    def next_gen(self):
        # top 2 in each species, top #3 overall
        species = self.speciate()
        pool = []



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

        return species



    def update(self,segments):
        for c in self.cars:
            c.update(segments, self.goal)


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