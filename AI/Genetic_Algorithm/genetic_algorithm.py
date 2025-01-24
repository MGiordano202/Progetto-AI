from AI.Genetic_Algorithm.population.population import generate_initial_population
from AI.Genetic_Algorithm.fitness import calculate_fitness
from AI.Genetic_Algorithm.population.population import next_generation


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
        self.population = generate_initial_population(self.grid, self.player_start, self.player_goal, self.population_size)

    def evaluate_fitness(self):
        """Calcola il fitness per ogni individuo nella popolazione."""
        for i, individual in enumerate(self.population):
            # Debug per verificare il genome prima della valutazione
            if not isinstance(individual.genome, list):
                print(f"Errore: Genome di Individuo {i} non è una lista! Valore={individual.genome}")

            calculate_fitness(individual, self.grid, self.player_start, self.player_goal)
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def run(self):
        """Esegue l'algoritmo genetico."""
        self.initialize_population()
        # Aggiungi un controllo per il miglioramento della fitness
        no_improvement_generations = 0
        best_fitness_last_generation = None

        for generation in range(self.generations):
            print(f"Generazione {generation + 1}")

            self.evaluate_fitness()
            best_fitness = self.population[0].fitness
            print(f"Fitness migliore: {best_fitness}")

            # Controlla se la fitness è stabile
            if best_fitness_last_generation is not None and abs(best_fitness - best_fitness_last_generation) < 0.01:
                no_improvement_generations += 1
            else:
                no_improvement_generations = 0

            best_fitness_last_generation = best_fitness

            # Criterio di terminazione
            if best_fitness >= 2000:  # Raggiungimento obiettivo
                print("Obiettivo raggiunto!")
                break
            if no_improvement_generations >= 7:  # Fitness stabile per 10 generazioni
                print("Fitness stabile, terminazione.")
                break

            self.population = next_generation(
                self.population,
                self.mutation_rate,
                self.tournament_size
            )

        return self.population[0]
