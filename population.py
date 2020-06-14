import numpy as np
from car import Car
from mapdata import *
from neural_net import *
from p5 import *
from Integer import Integer
import random

inputs = 14
outputs = 2

class Population:


    def __init__(self, racetrack, size):
        self.changes=[]
        self.size = size
        self.innovation = 0
        self.success = 0
        self.biggestNode =0
        self.checkpoints = racetrack.checkpoints
        startx = racetrack.start.x
        starty = racetrack.start.y
        self.start = Point(startx,starty)
        self.goal = Point(racetrack.end.x,racetrack.end.y)

        ratio = (self.goal.y - self.start.y) / (self.goal.x - self.start.x)
        angle = degrees(atan(ratio))
        if (self.goal.x < self.start.x):
            angle += 180

        self.cars = [Car(startx, starty, angle,None) for i in range(size)]
        self.crashed_cars = []


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
        i =0
        j =0
        issues = []
        while(i < len(genome1) and j<len(genome2)):
            # overlap
            if genome1[i].innovation == genome2[j].innovation:
                if np.random.randint(0, 2) == 0:
                    new_genome.append(genome1[i].copy())
                else:
                    new_genome.append(genome2[j].copy())

            # disjoint
            elif genome1[i].innovation != genome2[j].innovation:
                if genome1[i].innovation < genome2[j].innovation:
                    new_genome.append(genome1[i].copy())
                    j -= 1

                else:
                    new_genome.append(genome2[j].copy())
                    i -= 1

                issues.append(len(new_genome) - 1)

            # car1 genome is longer
            if j == len(genome2)-1:
                if(i != len(genome1)-1):
                    excess = genome1[i+1:].copy()

                issues += list(np.arange(len(new_genome), len(excess)))

            i+=1
            j+=1


        new_genome += excess
        for i in issues:
            if self.isAncestor(new_genome[i],new_genome[i],new_genome):
                new_genome.remove(i)

        return new_genome



    def connectionSort(self,connection):
        return connection.innovation


    def next_gen(self):
        print("cars:" + str(len(self.cars)))
        print("Innov:" + str(self.innovation))

        self.cars += self.crashed_cars

        # top 2 in each species, top #3 overall
        species = self.speciate()
        numspecies = len(species)
        print("Species:" + str(numspecies))
        pool = []
        for specie in species:
            specie.sort(reverse=True, key=self.fitness)
            for i in range(min(4, len(specie))):
                pool.append(specie[i])

        self.cars.sort(reverse=True, key=self.fitness)
        best = self.cars[:min(int(0.2*self.size),len(self.cars))]

        pool += best
        pool += best

        # car that has made it to goal
        nextGEN = []
        if (self.fitness(self.cars[0]) == 1000):
            nextGEN.append(self.cars[0])
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


    def next_gen2(self, sub_pool):

        self.sub_pool.sort(reverse=True, key=self.fitness)
        best = self.sub_pool[:int(0.2 * len(sub_pool))]

        pool = []
        for i in range(len(best)):
            pool += [best[i]] * (len(best) - i)

        # car that has made it to goal
        nextGEN = []
        if (self.fitness(self.cars[0]) == 1000):
            nextGEN.append(self.cars[0])
        for i in range(self.size):

            randcar = pool[np.random.randint(0, len(pool))]
            randcar2 = pool[np.random.randint(0, len(pool))]
            parents = [randcar, randcar2]
            parents.sort(reverse=True, key=self.fitness)
            genome = self.crossover(parents[0], parents[1])

            self.mutation(genome)

            net = NeuralNet(genome)
            ratio = (self.goal.y - self.start.y) / (self.goal.x - self.start.x)
            angle = degrees(atan(ratio))
            if (self.goal.x < self.start.x):
                angle += 180
            nextGEN.append(Car(self.start.x, self.start.y, angle, net))

        return nextGEN






    def mutation(self,genome):
        # 80% nothing happens
        # 17% change weight
        # 2% add node/connection
        rand = np.random.randint(100)
        if(rand<80):
            return genome
        elif(rand<97):
            gene =genome[np.random.randint(len(genome))]
            gene.weight *= (1 + np.random.uniform(-0.1,0.1))
        else:
            rand = np.random.randint(2)
            if(rand==0):
                gene = genome[np.random.randint(len(genome))]
                biggest_ID = self.biggestNode
                self.biggestNode+=1

                parent = gene.in_ID
                child = gene.out_ID

                conn1 = NodeConnection(self.innovation,parent,biggest_ID,np.random.uniform(-1,1),np.random.uniform(-1,1))
                self.innovCheck(conn1)

                conn2 = NodeConnection(self.innovation,biggest_ID,child,np.random.uniform(-1,1),np.random.uniform(-1,1))
                self.innovCheck(conn2)

                genome.remove(gene)
                genome.append(conn1)
                genome.append(conn2)
            else:
                possible_parent = None
                junk_indicies = []
                bottom_node = None
                top_node = None
                while possible_parent is None and len(junk_indicies) < len(genome):
                    num = np.random.randint(len(genome))
                    possible_parent = None

                    while (num in junk_indicies):
                        num = np.random.randint(len(genome))

                    bottom_node = genome[num]
                    for top_node in genome:
                        if(top_node.out_ID == bottom_node.out_ID):
                            junk_indicies.append(num)
                            continue

                        if self.isAncestor(bottom_node,top_node,genome):
                            junk_indicies.append(num)
                            continue

                        possible_parent = top_node


                newconn = NodeConnection(self.innovation,top_node.in_ID,bottom_node.out_ID,np.random.uniform(-1,1),bottom_node.out_bias)
                self.innovCheck(newconn)

                genome.append(newconn)

    def isAncestor(self,start,search,genome):
        if(isinstance(start.out_ID,str)):
            return False
        if start.out_ID == search.in_ID:
            return True
        result = False
        for gene in genome:
            if gene.in_ID == start.out_ID:
                result = result or self.isAncestor(gene,start,genome)
            if result == True:
                return True




    def innovCheck(self,conn):
        changed = False
        for i in range(len(self.changes)):
            if (conn.isSameConn(self.changes[i])):
                conn.innovation = self.changes[i].innovation
                changed = True
        if (not changed):
            self.innovation += 1
            self.changes.append(conn)

    def fitness(self,car):
        penalty = 0
        if car.is_crashed:
            penalty = 500

        far = distance((car.x,car.y),self.goal)
        if far<=10:
            file = open("cars/" + str(self.success) + ".txt", "w")
            for gene in car.neural_net.genome:
                file.write(str(gene) + "\n")
            file.close()
            self.success += 1
            return 1000 - penalty

        checkpoint_reward = 900.0*car.sector/len(self.checkpoints)
        return -1*far - penalty + checkpoint_reward


    def speciate(self):
        species = []
        speciated = []
        num_species = 0
        for i in range(len(self.cars)):
            if(i in speciated):
                continue
            species.append([])
            species[num_species].append(self.cars[i])
            for j in range(i,len(self.cars)):
                if self.cars[i].neural_net.compareNets(self.cars[j].neural_net):
                    species[num_species].append(self.cars[j])
                    speciated.append(j)
            num_species+=1

        return species



    def update(self,segments,see):

        self.cars.sort(reverse=True,key=self.fitness)
        for c in self.cars:
            if(self.goal.x==0 and c.x <= self.checkpoints[c.sector].x):
                c.sector+=1

            if (self.goal.x != 0 and c.x >= self.checkpoints[c.sector].x):
                c.sector += 1

            c.update(segments,self.checkpoints[c.sector],see)
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



    def initialize_population(self,From_save):
        if(From_save != None):
            genome=[]
            self.size=1
            with open("cars/"+From_save+".txt", "r") as file:
                allines = file.readlines()
                for i in range(len(allines)):
                    parts = allines[i].strip().split(",")
                    genome.append(NodeConnection(parts[0],parts[1],parts[2],parts[3],parts[4]))
            self.cars[0].neural_net= NeuralNet(genome)


        self.innovation = inputs*outputs
        for c in self.cars:
            genome = []
            for outs in range(outputs):
                for ins in range(inputs):

                    genome.append(NodeConnection(outs * inputs + ins, "in_" + str(ins), "out_" + str(outs), np.random.randn(), np.random.randn()))

            c.neural_net = NeuralNet(genome)



class NodeConnection:
    def __init__(self,innovation, in_ID, out_ID, weight, out_bias):
        self.innovation = innovation
        self.out_bias = out_bias
        self.in_ID = in_ID
        self.out_ID = out_ID
        self.weight = weight
    def isSameConn(self, other):
        if(isinstance(other,NodeConnection)):
            return str(self.in_ID) == str(other.in_ID) and str(self.out_ID) == str(other.out_ID)
        return False
    def copy(self):
        return NodeConnection(self.innovation, self.in_ID, self.out_ID, self.weight, self.out_bias)
    def __str__(self):
        return str(self.innovation)+","+str(self.out_ID)+","+str(self.in_ID)+","+str(self.weight)+","+str(self.out_bias)