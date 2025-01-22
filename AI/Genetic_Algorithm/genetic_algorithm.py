from AI.Genetic_Algorithm.population import generate_initial_population
from AI.Genetic_Algorithm.fitness import calculate_fitness
from AI.Genetic_Algorithm.population import next_generation


class GeneticAlgorithm:
    def __init__(self, grid, player_start, player_goal, population_size, generations, mutation_rate, tournament_size):
        self.grid = grid
        self.player_start = player_start
        self.player_goal = player_goal
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.population = []

    def initialize_population(self):
        """Genera la popolazione iniziale."""
        self.population = generate_initial_population(self.population_size, 100, self.grid.size)

    def evaluate_fitness(self):
        """Calcola il fitness per ogni individuo nella popolazione."""
        for individual in self.population:
            calculate_fitness(individual, self.grid, self.player_start, self.player_goal)
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def run(self):
        """Esegue l'algoritmo genetico."""
        self.initialize_population()

        for generation in range(self.generations):
            print(f"Generazione {generation + 1}")
            self.evaluate_fitness()
            best_fitness = self.population[0].fitness

            if best_fitness >= 1000:
                print("Obiettivo raggiunto!")
                break

            self.population = next_generation(self.population, self.mutation_rate, self.tournament_size)

        return self.population[0]
