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
        self.best_individuals = []  # Per monitorare il migliore di ogni generazione

    def initialize_population(self):
        """Genera la popolazione iniziale."""
        self.population = generate_initial_population(self.grid,
                                                      self.player_start,
                                                      self.player_goal,
                                                      self.population_size
                                                    )

    def evaluate_fitness(self):
        """Calcola il fitness per ogni individuo nella popolazione."""
        for i, individual in enumerate(self.population):
            try:
                calculate_fitness(individual, self.grid, self.player_start, self.player_goal)
            except Exception as e:
                print(f"Errore nel calcolo della fitness per individuo {i}: {e}")

        # Ordina la popolazione in base alla fitness, in ordine decrescente
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def save_best_individual(self, generation):
        """Salva il miglior individuo di ogni generazione."""
        best_individual = self.population[0]
        self.best_individuals.append((generation, best_individual.fitness, best_individual.genome))
        print(f"[DEBUG] Miglior individuo generazione {generation}: Fitness={best_individual.fitness}, Genome={best_individual.genome}")

    def run(self):
        """Esegue l'algoritmo genetico."""
        self.initialize_population()

        no_improvement_generations = 0
        best_fitness_last_generation = None

        for generation in range(self.generations):
            print(f"Generazione {generation + 1}")

            # Valutazione della fitness
            self.evaluate_fitness()

            # Salva e stampa il miglior individuo della generazione
            self.save_best_individual(generation + 1)

            best_fitness = self.population[0].fitness
            print(f"Fitness migliore: {best_fitness}")

            # Controlla miglioramenti della fitness
            if best_fitness_last_generation is not None and abs(best_fitness - best_fitness_last_generation) < 0.01:
                no_improvement_generations += 1
            else:
                no_improvement_generations = 0
            best_fitness_last_generation = best_fitness

            # Criterio di terminazione: fitness target raggiunta
            if best_fitness >= 1040:
                print("Obiettivo raggiunto!")
                break

            # Criterio di terminazione: fitness stabile
            if no_improvement_generations >= 10:
                print("Fitness stabile, terminazione anticipata.")
                break

            # Genera la nuova generazione
            self.population = next_generation(
                self.population,
                self.mutation_rate,
                self.tournament_size,
                self.grid,
                self.player_goal
            )

        # Restituisci il miglior individuo finale
        return self.population[0]
