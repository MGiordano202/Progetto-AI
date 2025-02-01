from AI.Genetic_Algorithm.individual import Individual
from AI.a_star import Astar


def best_segment_crossover(parent1, parent2, goal, start, grid):
    """
    Esegue un crossover ibrido basato sui segmenti migliori dei genitori.
    :param grid:
    :param start:
    :param parent1: Primo genitore (oggetto Individual)
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
    segment_size2 = max(1, len(genome2) // num_segments)

    # Divide in segmenti (assicurati di coprire l'intero genoma)
    segments1 = []
    segments2 = []

    for i in range(segment_size1, len(genome1), segment_size1):
        segments1.append(genome1[i:i + segment_size1])

    for i in range(segment_size2, len(genome2), segment_size2):
        segments2.append(genome2[i:i + segment_size2])

    # Seleziona i migliori segmenti alternativamente
    child1_genome = [start]  # Inserisci la posizione iniziale
    child2_genome = [start]  # Inserisci la posizione iniziale

    for seg1, seg2 in zip(segments1, segments2):
        fitness_seg1 = sum(manhattan_distance(coord, goal) for coord in seg1)
        fitness_seg2 = sum(manhattan_distance(coord, goal) for coord in seg2)

        if fitness_seg1 < fitness_seg2:
            child1_genome.extend(seg1 if child1_genome[-1] == seg1[0] else seg1[1:])
        else:
            child1_genome.extend(seg2 if child1_genome[-1] == seg2[0] else seg2[1:])

        if fitness_seg2 < fitness_seg1:
            child2_genome.extend(seg2 if child2_genome[-1] == seg2[0] else seg2[1:])
        else:
            child2_genome.extend(seg1 if child2_genome[-1] == seg1[0] else seg1[1:])

    if not is_valid_genome(child1_genome, start):
        child1_genome = repair_genome(child1_genome, goal, grid)
    if not is_valid_genome(child2_genome, start):
        child2_genome = repair_genome(child2_genome, goal, grid)

    child1 = Individual(genome=child1_genome)
    child2 = Individual(genome=child2_genome)

    return child1, child2

def extend_genome(current_genome, segment):
    """
    Aggiunge un segmento al genoma corrente, evitando duplicazioni se il segmento inizia già
    con l'ultimo elemento del genoma corrente.
    """
    if current_genome[-1] == segment[0]:
        return current_genome + segment[1:]
    else:
        return current_genome + segment

def is_valid_genome(genome, start_position):
    """
    Verifica che il percorso:
      - Inizi dalla posizione di partenza.
      - Ogni coppia di nodi consecutivi sia adiacente (distanza Manhattan pari a 1).
    """
    if genome[0] != start_position:
        return False

    for i in range(1, len(genome)):
        if manhattan_distance(genome[i], genome[i - 1]) != 1:
            return False
    return True

def repair_genome(genome, goal, grid):
    """
    Ripara un genoma utilizzando A* per riconnettere le parti "rotte".
    Scorre il genoma e, ogni volta che trova un passo non valido,
    utilizza A* per calcolare il percorso corretto dal punto corrente al target desiderato.
    """
    repaired_genome = [genome[0]]  # Inizia dalla prima posizione
    astar = Astar(grid)

    i = 1
    while i < len(genome):
        current = repaired_genome[-1]
        next_coord = genome[i]
        if manhattan_distance(current, next_coord) == 1 and grid.is_passable(*next_coord):
            repaired_genome.append(next_coord)
            i += 1
        else:
            path_segment, _ = astar.find_path(current, next_coord)
            if path_segment is None:
                break
            if path_segment[0] == current:
                path_segment = path_segment[1:]
            repaired_genome.extend(path_segment)
            i += 1

    if repaired_genome[-1] != goal:
        path_segment, _ = astar.find_path(repaired_genome[-1], goal)
        if path_segment is not None:
            if path_segment[0] == repaired_genome[-1]:
                path_segment = path_segment[1:]
            repaired_genome.extend(path_segment)

    return repaired_genome

def manhattan_distance(coord1, coord2):
    """
    Calcola la distanza di Manhattan tra due coordinate.
    :param coord1: Prima coordinata (tuple).
    :param coord2: Seconda coordinata (tuple).
    :return: Distanza di Manhattan.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
