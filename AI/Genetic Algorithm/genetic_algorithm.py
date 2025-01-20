import random
from population import generate_initial_population
from fitness import calculate_fitness
from Operators.Selection.tournament_selection import tournament_selection
from Operators.Crossover.single_point_crossover import single_point_crossover
from Operators.Mutation.random_mutation import random_mutation

def genetic_algorithm(grid, player_goal, population_size, generations, mutation_rate, tournament_size):
    population = generate_initial_population(population_size, grid.size)

    for generation in range(generations):
        print(f"Generazione {generation + 1}")

        # Calcola il fitness di ogni individuo
        for individual in population:
            calculate_fitness(individual, grid, player_goal)

        # Ordina la popolazione in base alla fitness
        population.sort(key=lambda x: x.fitness, reverse=True)
        print(f"Fitness migliore: {population[0].fitness}")

        # Condizione di terminazione
        if population[0].fitness >= 1000:
            print("Obiettivo raggiunto!")
            break

        # Genera la nuova generazione
        new_population = []

        elitism_count = max(1, population_size // 10) # Mantiene il 10% della popolazione migliore
        new_population.extend(population[:elitism_count])

        # Genera il resto della popolazione
        while len(new_population) < population_size:
            # Seleziona i genitori
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)

            # Crossover
            child = single_point_crossover(parent1, parent2)

            # Mutazione
            child = random_mutation(child, mutation_rate)

            new_population.append(child)

        population = new_population

    return population[0] # Restituisce il miglior individuo
