import random
from individual import Individual
###DA RIVEDERE
class Population:
    def __init__(self, size, seq_length):
        self.size = size
        self.seq_length = seq_length
        self.individuals = []


    def initialize(self):
        self.individuals =  [Individual.random(self.seq_length) for _ in range(self.size)]

    def update(self, new_individuals):
        self.individuals = new_individuals

    def get_best_individual(self, fitnesses):
        best_index = fitnesses.index(max(fitnesses))
        return self.individuals[best_index]