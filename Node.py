from numpy import *
class Node:
    def __init__(self,parents,weights,bias,ID):
        self.val = 0
        self.parents = parents
        self.weights = weights
        self.bias = bias
        self.ID = ID
    def getval(self):
        if len(self.parents) == 0 :
            return self.val
        else:
            sum = 0
            for i in range(len(self.parents)):
                sum += self.parents[i].getval()*self.weights[i]
            sum+=self.bias
            return tanh(sum)
    def sigmoid(self,x):
        return 1/(1+math.exp(-x))