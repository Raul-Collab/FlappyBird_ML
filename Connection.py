import random

class Connection():
    def __init__(self, origin_node, dest_node, weight):
        self.origin_node = origin_node
        self.dest_node = dest_node
        self.weight = weight

    def mutate_weight(self):
        if random.uniform(0, 1) < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1)/10
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    def clone(self, origin_node, dest_node):
        clone = Connection(origin_node, dest_node, self.weight)
        return clone