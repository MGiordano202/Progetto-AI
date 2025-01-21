import random
from AI.Genetic_Algorithm.individual import Individual
from AI.Genetic_Algorithm.population import generate_initial_population
from AI.Genetic_Algorithm.fitness import calculate_fitness
from AI.Genetic_Algorithm.Operators.Selection.tournament_selection import tournament_selection
from AI.Genetic_Algorithm.Operators.Crossover.single_point_crossover import single_point_crossover
from AI.Genetic_Algorithm.Operators.Mutation.random_mutation import random_mutation


class GeneticAlgorithm:
    def __init__(self, grid, player_goal, population_size, generations, mutation_rate, tournament_size):
        self.grid = grid
        self.player_goal = player_goal
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.population = []

    def initialize_population(self):
        """Genera la popolazione iniziale."""
        self.population = generate_initial_population(self.population_size, self.grid.rows)

    def evaluate_fitness(self):
        """Calcola il fitness per ogni individuo nella popolazione."""
        for individual in self.population:
            calculate_fitness(individual, self.grid, self.player_goal)
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def evolve(self):
        """Evolve la popolazione per una generazione."""
        new_population = []
        elitism_count = max(1, self.population_size // 10)
        new_population.extend(self.population[:elitism_count])

        while len(new_population) < self.population_size:
            parent1 = tournament_selection(self.population, self.tournament_size)
            parent2 = tournament_selection(self.population, self.tournament_size)
            child = single_point_crossover(parent1, parent2)
            child = random_mutation(child, self.mutation_rate)
            new_population.append(child)

        self.population = new_population

    def run(self):
        """Esegue l'algoritmo genetico."""
        self.initialize_population()

        for generation in range(self.generations):
            print(f"Generazione {generation + 1}")
            self.evaluate_fitness()
            print(f"Fitness migliore: {self.population[0].fitness}")

            if self.population[0].fitness >= 1000:
                print("Obiettivo raggiunto!")
                break

            self.evolve()

        return self.population[0]
