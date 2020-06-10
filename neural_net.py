from Node import Node
import numpy as np

class NeuralNet:
    def __init__(self, genome):

        self.neuralnet =None
        self.size = len(genome)
        self.genome = genome
        node_IDs = set([])
        for connection in genome:
            node_IDs.add(connection.out_ID)
            node_IDs.add(connection.in_ID)

        nodes = [None]*len(node_IDs)
        input_nodes = []
        output_nodes = []
        for n in node_IDs:
            ID = n
            if isinstance(n,str):
                type = ID.split("_")[0]
                val = int(ID.split("_")[1])
                if(type == "out"):
                    output_nodes.append(Node([],[],0,n))
                elif type == "in":
                    input_nodes.append(Node([], [], 0,n))
            else:
                nodes[n] = Node([],[],0,n)

        output_nodes.sort(reverse=True, key=self.compare)
        input_nodes.sort(reverse=True, key=self.compare)

        for connection in genome:
            node0_ID = connection.in_ID
            node1_ID = connection.out_ID
            weight = connection.weight
            bias = connection.out_bias

            #finds the correct node for parent
            if(isinstance(node0_ID,str)):
                type = node0_ID.split("_")[0]
                val = int(node0_ID.split("_")[1])
                if (type == "out"):
                    node0 = output_nodes[val]
                else:
                    node0 = input_nodes[val]
            else:
                node0 = nodes[node0_ID]

            #finds node for child
            if (isinstance(node1_ID, str)):
                type = node1_ID.split("_")[0]
                val = int(node1_ID.split("_")[1])
                if (type == "out"):
                    node1 = output_nodes[val]
                else:
                    node1 = input_nodes[val]
            else:
                node1 = nodes[node1_ID]

            #sets child with weight bias and parent
            node1.parents.append(node0)
            node1.weights.append(weight)
            node1.bias = bias

        self.input_nodes = input_nodes
        self.output_nodes = output_nodes

    def print_net(self):
        for out_node in self.output_nodes:
            for parent in out_node.parents:
                print(parent.ID)
                print("      " + str(out_node.ID))

    def connectionSort(self,connection):
        return connection.innovation

    def compareNets(self,net):
        if len(net.genome)!=len(self.genome):
            return False
        net.genome.sort(reverse=True, key=self.connectionSort)
        self.genome.sort(reverse=True, key=self.connectionSort)
        for i in range(len(self.genome)):
            if(net.genome[i].innovation != self.genome[i].innovation):
                False
        return True
        # out_number
        # in_number

        # go through genome and sum number of unique nodes
        # make all new nodes put them in array by ID with inputs and outputs in a different arrays
        # make connections by adding parent to nodes
    def compare(self,node):
        if(isinstance(node.ID,str)):
            return int(node.ID.split("_")[1])
        else:
            return node.ID

    def answer_to_everything(self, inputs):
        for i in range(len(inputs)):
            self.input_nodes[i].val = inputs[i]

        outputs = [n.getval() for n in self.output_nodes]

        return outputs



