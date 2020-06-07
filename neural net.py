class NeuralNet:
    def __init__(self, layer_node_weight_pairing):
        # layer weight pairing contains the layers as its first array with the
        # nodes as its second dimension and there weights in the third
        # the second and third dimensions will be the same size that of the number of neurons in that layer
        # this is a poor way of handling a net but the most compact way of transporting it
        # as of now the idea is to make a 2 d array of all the nodes ( this makes me think that an array wouldnt actually be that bad)
        # after all the nodes are only doing part of a dot product and we only get rid of 1 dimension)

        self.neuralnet =None
        self.size = len(layer_node_weight_pairing)

    def answer_to_everything(self, inputs):
        for n, i in self.neuralnet[0], inputs:
            n.val = i

        output = [None]*len(self.neuralnet[self.size-1])
        output = [n.getval() for n in self.neuralnet[self.size - 1]]
        # for n, i in self.neuralnet[self.size-1], range(len(output)):
        #   output= n.getval()

        return output
