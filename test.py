from AI.Genetic_Algorithm.Operators.Crossover.best_segment_crossover import repair_genome
from AI.Genetic_Algorithm.Operators.Mutation.segment_mutation import segment_mutation
import random
from AI.Genetic_Algorithm.individual import Individual
from grid import Grid

random.seed(42)  # Per ottenere risultati riproducibili

grid = Grid(5, 5)
grid.generate_bomberman_map()  # Genera una mappa casuale con muri e blocchi

original_path = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)]  # Percorso iniziale valido
individual = Individual(genome=original_path)

mutated_individual = segment_mutation(individual, mutation_rate=0.5, grid=grid)

assert mutated_individual is not None, "La mutazione ha restituito None"
assert mutated_individual.genome != original_path, "Il percorso non è cambiato"
assert mutated_individual.genome[0] == original_path[0], "Il punto di partenza è cambiato!"
assert mutated_individual.genome[-1] == original_path[-1], "Il punto di arrivo è cambiato!"
