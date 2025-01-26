from AI.Genetic_Algorithm.individual import Individual


def best_segment_crossover(parent1, parent2, goal, start, grid):
    """
    Esegue un crossover ibrido basato sui segmenti migliori dei genitori.
    :param grid:
    :param start:
    :param parent1: primo genitore (oggetto Individual)
    :param parent2: secondo genitore (oggetto Individual)
    :param goal: posizione dell'obiettivo (tuple)
    :return: due nuovi figli (oggetti Individual)
    """
    if not isinstance(parent1, Individual) or not isinstance(parent2, Individual):
        raise TypeError("I genitori devono essere oggetti di tipo 'Individual'")

    genome1, genome2 = parent1.genome, parent2.genome

    # Suddivide i genomi in segmenti
    num_segments = 5
    segment_size1 = max(1, len(genome1) // num_segments)
    segment_size2 = max(1, len(genome1) // num_segments)

    # Divide in segmenti (assicurati di coprire l'intero genoma)
    segments1 = []
    segments2 = []

    for i in range(0, len(genome1), segment_size1):
        if i != 0:
            segments1.append(genome1[i:i + segment_size1])

    for i in range(0, len(genome2), segment_size2):
        if i != 0:
            segments2.append(genome2[i:i + segment_size2])

    # Seleziona i migliori segmenti alternativamente
    child1_genome = [start]  # Inserisci la posizione iniziale
    child2_genome = [start]  # Inserisci la posizione iniziale

    for seg1, seg2 in zip(segments1, segments2):
        fitness_seg1 = sum(manhattan_distance(coord, goal) for coord in seg1)
        fitness_seg2 = sum(manhattan_distance(coord, goal) for coord in seg2)

        if fitness_seg1 < fitness_seg2:
            child1_genome.extend(seg1[1:]) # Aggiungi il resto del segmento senza la posizione iniziale
        else:
            child1_genome.extend(seg2[1:])

        if fitness_seg2 < fitness_seg1:
            child2_genome.extend(seg2[1:])
        else:
            child2_genome.extend(seg1[1:])

    if not is_valid_genome(child1_genome, start):
        child1_genome = repair_genome(child1_genome, goal, grid)
    if not is_valid_genome(child2_genome, start):
        child2_genome = repair_genome(child2_genome, goal, grid)

    child1 = Individual(genome=child1_genome)
    child2 = Individual(genome=child2_genome)

    return child1, child2

def is_valid_genome(genome, start_position):
    # Controlla che il percorso inizi dalla posizione iniziale
    if genome[0] != start_position:
        return False
    # Controlla che ogni posizione sia adiacente alla precedente
    for i in range(1, len(genome)):
        if manhattan_distance(genome[i], genome[i-1]) != 1:
            return False
    return True

def repair_genome(genome, goal, grid):
    """
    Ripara un genoma per garantire che sia valido (inizia da (1,1) e sia lineare).
    """
    repaired_genome = [genome[0]]  # Inizia dalla prima posizione
    for coord in genome[1:]:
        # Controlla se la posizione corrente è valida rispetto all'ultima valida
        if manhattan_distance(repaired_genome[-1], coord) == 1 and grid.is_passable(*coord):
            repaired_genome.append(coord)
        else:
            # Trova un percorso valido dalla posizione precedente
            repaired_genome = reconnect_path(repaired_genome, coord, grid)

    # Assicurati che l'obiettivo sia raggiunto alla fine del percorso
    if repaired_genome[-1] != goal:
        repaired_genome = reconnect_path(repaired_genome, goal, grid)

    return repaired_genome


def reconnect_path(path, target, grid):
    """
    Riconnette il percorso a una posizione target creando un collegamento lineare.
    Evita cicli durante la riconnessione.
    :param path: Il percorso corrente (lista di tuple).
    :param target: La posizione target (tuple).
    :param grid: Oggetto griglia che verifica se le posizioni sono passabili.
    :return: Un percorso riconnesso.
    """

    visited = set(path)  # Tiene traccia delle posizioni già visitate
    current = path[-1]  # Posizione attuale
    while current != target:
        if current[0] < target[0]:  # Spostati verso il basso
            next_pos = (current[0] + 1, current[1])
        elif current[0] > target[0]:  # Spostati verso l'alto
            next_pos = (current[0] - 1, current[1])
        elif current[1] < target[1]:  # Spostati verso destra
            next_pos = (current[0], current[1] + 1)
        elif current[1] > target[1]:  # Spostati verso sinistra
            next_pos = (current[0], current[1] - 1)


        # Controlla che la posizione sia valida e non visitata
        if grid.is_passable(*next_pos) and next_pos not in visited:
            path.append(next_pos)
            visited.add(next_pos)
            current = next_pos
        else:
            # Interrompi se non ci sono mosse valide
            break

    return path


def manhattan_distance(coord1, coord2):
    """
    Calcola la distanza di Manhattan tra due coordinate.
    :param coord1: Prima coordinata (tuple).
    :param coord2: Seconda coordinata (tuple).
    :return: Distanza di Manhattan.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
