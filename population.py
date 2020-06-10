import numpy as np
from car import Car
from mapdata import *
from neural_net import *
from p5 import *
import random

inputs = 14
outputs = 2

class Population:


    def __init__(self, racetrack, size):
        self.size = size
        self.innovation = 0
        startx = racetrack.start.x
        starty = racetrack.start.y
        self.start = Point(startx,starty)
        self.goal = Point(racetrack.end.x,racetrack.end.y)

        ratio = (self.goal.y - self.start.y) / (self.goal.x - self.start.x)
        angle = degrees(atan(ratio))
        if (self.goal.x < self.start.x):
            angle += 180

        self.cars = [Car(startx, starty, angle,None) for i in range(size)]


    def crossover(self, car1, car2):
        # car1 more fit

        genome1 = car1.neural_net.genome
        genome2 = car2.neural_net.genome

        genome1.sort(reverse=True, key=self.connectionSort)
        genome2.sort(reverse=True, key=self.connectionSort)

        # in both (randomly choose from 1 if gene is common between the two)
        # disjoint = not in other car (all disjoints passed down)
        # excess : from longer genome (larger innov num than other car) (excess passed from fitter car)

        new_genome = []
        excess = []
        max_innov_genome1 = 0
        max_innov_genome2 = 0
        i =0
        j =0
        while(i < len(genome1) and j<len(genome2)):
            max_innov_genome1 += 1
            max_innov_genome2 += 1


            # overlap
            if genome1[i].innovation == genome2[j].innovation:
                if np.random.randint(0, 2) == 0:
                    new_genome.append(genome1[i])
                else:
                    new_genome.append(genome2[j])

            # disjoint
            elif genome1[i].innovation != genome2[j].innovation:
                if genome1[i].innovation < genome2[j].innovation:
                    new_genome.append(genome1[i])
                    j -= 1

                else:
                    new_genome.append(genome2[j])
                    i -= 1

            # car1 genome is longer
            if j == len(genome2)-1:
                excess = genome1[i:]

            i+=1
            j+=1

        new_genome += excess
        return new_genome



    def connectionSort(self,connection):
        return connection.innovation


    def next_gen(self):
        if(len(self.cars) == 0):
            ratio = (self.goal.y - self.start.y) / (self.goal.x - self.start.x)
            angle = degrees(atan(ratio))
            if (self.goal.x < self.start.x):
                angle += 180
            self.cars = [Car(self.start.x,self.start.y,angle, None) for i in range(self.size)]
            self.initialize_population()
            return

        # top 2 in each species, top #3 overall
        species = self.speciate()
        numspecies = len(species)
        pool = []
        for specie in species:
            specie.sort(reverse=True, key=self.fitness)
            pool.append(specie[0])

        self.cars.sort(reverse=True, key=self.fitness)
        best = self.cars[:min(5,len(self.cars))]
        pool += best

        nextGEN = []
        for i in range(self.size):

            randcar = pool[np.random.randint(0,len(pool))]
            randcar2 = pool[np.random.randint(0,len(pool))]
            parents = [randcar,randcar2]
            parents.sort(reverse=True, key=self.fitness)
            genome = self.crossover(parents[0],parents[1])

            self.mutation(genome)

            net = NeuralNet(genome)
            ratio=(self.goal.y-self.start.y)/(self.goal.x-self.start.x)
            angle = degrees(atan(ratio))
            if (self.goal.x < self.start.x):
                angle +=180
            nextGEN.append(Car(self.start.x,self.start.y,angle,net))


        self.cars = nextGEN

    def mutation(self,genome):
        # 80% nothing happens
        # 15% change weight
        # 5% add node/connection
        rand = np.random.randint(100)
        if(rand<80):
            return genome
        elif(rand<95):
            gene =genome[np.random.randint(len(genome))]
            gene.weight *= (1 + np.random.uniform(-0.1,0.1))
        else:
            rand = np.random.randint(2)
            if(rand==0):
                gene = genome[np.random.randint(len(genome))]
                nodes = set()
                for g in genome:
                    nodes.add(g.in_ID)
                    nodes.add(g.out_ID)
                biggest_node=len(nodes)-inputs-outputs
                parent = gene.in_ID
                child = gene.out_ID

                conn1 = NodeConnection(self.innovation,parent,biggest_node+1,np.random.uniform(-1,1),np.random.uniform(-1,1))
                self.innovation += 1
                conn2 = NodeConnection(self.innovation,biggest_node+1,child,np.random.uniform(-1,1),np.random.uniform(-1,1))
                self.innovation += 1

                genome.remove(gene)
                genome.append(conn1)
                genome.append(conn2)
            else:
                all_possible_parents = set()
                out = 0
                junk_indicies =[]
                while(len(all_possible_parents) == 0 and len(junk_indicies) < len(genome)):
                    num =np.random.randint(len(genome))
                    while (num in junk_indicies):
                        num = np.random.randint(len(genome))
                    gene = genome[num]
                    out = gene.out_ID
                    for g in genome:
                        if(g.out_ID == gene.out_ID):
                            continue
                        all_possible_parents.add(g.in_ID)

                if(len(junk_indicies)<len(genome)):
                    return
                in_id = random.choice(list(all_possible_parents))
                newconn = NodeConnection(self.innovation,in_id,out,np.random.uniform(-1,1),np.random.uniform(-1,1))
                self.innovation+=1
                genome.append(newconn)


    def fitness(self,car):
        far = distance((car.x,car.y),self.goal)
        if far<=10:
            return 10000

        return -1*far


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
            c.update(segments,self.goal)
            c.drawcar()


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



    def initialize_population(self):


        for c in self.cars:
            genome = []
            for outs in range(outputs):
                for ins in range(inputs):
                    self.innovation+=1
                    genome.append(NodeConnection(outs * inputs + ins, "in_" + str(ins), "out_" + str(outs), np.random.randn(), np.random.randn()))

            c.neural_net = NeuralNet(genome)



class NodeConnection:
    def __init__(self,innovation, in_ID, out_ID, weight, out_bias):
        self.innovation = innovation
        self.out_bias = out_bias
        self.in_ID = in_ID
        self.out_ID = out_ID
        self.weight = weight