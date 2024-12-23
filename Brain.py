import Node
import Connection
import random

class Brain:
    def __init__(self, inputs, clone = False, top_player = False, weights = []):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 2
        self.biasLayer = False
        self.weigths = weights

        if not clone:
            for i in range(0, self.inputs):
                self.nodes.append(Node.Node(i))
                self.nodes[i].layer = 0
            #Bias node
            if self.biasLayer == True:
                self.nodes.append(Node.Node(self.inputs))
                self.nodes[self.inputs].layer = 0

                #Output node
                self.nodes.append(Node.Node(self.inputs + 1))
                self.nodes[self.inputs + 1].layer = 1
            else:
                self.nodes.append(Node.Node(self.inputs))
                self.nodes[self.inputs].layer = 1
            
            #Create connections
            if not top_player:
                nodeSize = len(self.nodes)
                for i in range(0, nodeSize):
                    self.connections.append(Connection.Connection(self.nodes[i],
                                                        self.nodes[-1], 
                                                            random.uniform(-1, 1)))
            if top_player:
                self.make_top_player(self.weigths)

            
    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(0, len(self.connections)):
            self.connections[i].origin_node.connections.append(self.connections[i])
    
    def make_top_player(self, weights):
        nodeSize = len(self.nodes)
        for i in range(0, nodeSize):
            self.connections.append(Connection.Connection(self.nodes[i],
                                                self.nodes[-1], 
                                                    weights[i]))


    def generate_net(self):
        self.connect_nodes()
        self.net = []

        #Try without the below sorting once
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if j == self.nodes[i].layer:
                    self.net.append(self.nodes[i])

    def feed_forward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        if self.biasLayer == True:
            self.nodes[self.inputs].output_value = 1

        for i in range(0, len(self.net)):
            self.net[i].activation()

        if self.biasLayer == True:
            output_value = self.nodes[self.inputs + 1].output_value
            #print("Net: ", self.net[self.inputs + 1].layer)
        else:
            output_value = self.nodes[self.inputs].output_value

        #Try by only setting output node's input value to 0
        for i in range(0, len(self.nodes)):
            self.net[i].input_value = 0

        return output_value
    
    def clone(self):
        clone = Brain(self.inputs, True)

        for n in self.nodes:
            clone.nodes.append(n.clone())
        
        for c in self.connections:
            clone.connections.append(c.clone(clone.get_node(c.origin_node.index), 
                                             clone.get_node(c.dest_node.index)))
        
        clone.layers = self.layers
        clone.connect_nodes()
        return clone
    
    def get_node(self, id):
        for n in self.nodes:
            if n.index == id:
                return n
            
    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()
