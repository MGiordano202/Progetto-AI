def calculate_fitness(individual, grid, player_goal):
    """
        Calcola la fitness di un individuo.
        individual: un individuo da valutare.
        grid: la griglia di gioco.
        player_goal: l'obiettivo del giocatore.
        ritorna un valore fitness (più alto è meglio).
    """
    path = individual.path
    fitness = 0

    for index, (row, col, place_bomb) in enumerate (path):
        if not grid.is_passable(row, col): # Penalizza se la cella non è raggiungibile
            fitness -= 100
            continue

        # Premia se il giocare si avvicina all'obiettivo
        goal_distance = abs(player_goal[0] - row) + abs(player_goal[1] - col)
        fitness += 100 / (1 + goal_distance)

        # Premia se il giocatore distrugge blocchi che lo ostacolano
        if place_bomb:
            fitness += 50

    # Bonus se l'obiettivo è raggiunto
    if path[-1][:2] == player_goal:
        fitness += 1000

    individual.fitness = fitness
    return fitness