import operator
import math
import Species


class Population:

    #Variables
    x = []
    y = []

    def __init__(self, birds, game):
        self.generation = 1
        self.species = []
        self.birds = birds
        self.size = game.birdAmount

    def natural_selection(self):
        #print("Speciate")
        self.speciate()

        #print("CALCULATE FITNESS")
        self.calculate_fitness()

        self.kill_extinct()

        self.kill_stale()

        #print("SORT BY FITNESS")
        self.sort_species_by_fitness()

        #print("PRODUCE NEXT GEN")
        self.next_gen()

        weights = self.get_weights_of_top_player()
        print("Weights: ", weights )

    def get_weights_of_top_player(self):
        connections = self.species[0].players[0].brain.connections
        weights = []
        for c in connections:
            weights.append(c.weight)
        return weights
    
    def speciate(self):
        for s in self.species:
            s.birds = []
        
        for b in self.birds:
            add_to_species = False
            for s in self.species:
                if s.similarity(b.brain):
                    s.addBird(b)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(Species.Species(b))

    def calculate_fitness(self):
        for b in self.birds:
            b.calculate_fitness()
        for s in self.species:
            s.calculate_avg_fitness()
        
    def kill_extinct(self):
        species_bin = []
        for s in self.species:
            if len(s.players) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale(self):
        player_bin = []
        species_bin = []

        for s in self.species:
            if s.staleness > 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for p in s.players:
                        player_bin.append(p)
                else:
                    s.staleness = 0
        for p in player_bin:
            if p in self.birds:
                self.birds.remove(p)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_birds_by_fitness()
        
        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)
        print("Avg Fitness: ", self.species[0].average_fitness)

    def next_gen(self):
        children = []

        for s in self.species:
            children.append(s.champion.clone())
        
        children_per_species = math.floor(((self.size - len(self.species))/ len(self.species)))
        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())
            
        while len(children) < self.size:
            children.append(self.species[0].offspring())
        
        self.birds.clear()
        for child in children:
            self.birds.append(child)
        self.generation += 1
        