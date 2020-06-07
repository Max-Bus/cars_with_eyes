from numpy import *
class Node:
    def __init__(self,parents,weights,bias):
        self.val = 0
        self.parents = parents
        self.weights = weights
        self.bias = bias
    def getval(self):
        if self.parents == None:
            return self.val
        else:
            sum = 0;
            for p in self.parents:
                sum += p.getval
            sum+=self.bias
            return self.sigmoid(sum)
    def sigmoid(self,x):
        return 1/(1+math.exp(-x))