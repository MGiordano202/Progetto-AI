from grid import Grid
from AI.Genetic_Algorithm.individual import Individual


def best_segment_crossover(parent1, parent2, goal, start, grid):
    """
    Esegue un crossover ibrido basato sui segmenti migliori dei genitori.
    :param parent1: primo genitore (oggetto Individual)
    :param parent2: secondo genitore (oggetto Individual)
    :param goal: posizione dell'obiettivo (tuple)
    :return: due nuovi figli (oggetti Individual)
    """
    if not isinstance(parent1, Individual) or not isinstance(parent2, Individual):
        raise TypeError("I genitori devono essere oggetti di tipo 'Individual'")

    genome1, genome2 = parent1.genome, parent2.genome

    # Suddivide i genomi in segmenti
    num_segments = 3
    segment_size1 = len(genome1) // num_segments
    segment_size2 = len(genome2) // num_segments

    # Divide in segmenti (assicurati di coprire l'intero genoma)
    segments1 = [genome1[i:i + segment_size1] for i in range(0, len(genome1), segment_size1)]
    segments2 = [genome2[i:i + segment_size2] for i in range(0, len(genome2), segment_size2)]

    # Seleziona i migliori segmenti alternativamente
    child1_genome = [segments1[0][0]]  # Inserisci la posizione iniziale
    child2_genome = [segments2[0][0]]  # Inserisci la posizione iniziale

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

    child1_genome = repair_genome(child1_genome, goal, grid)
    child2_genome = repair_genome(child2_genome, goal, grid)

    child1 = Individual(genome=child1_genome)
    child2 = Individual(genome=child2_genome)

    return child1, child2

def repair_genome(genome, goal, grid):
    """
    Ripara un genoma per garantire che sia valido (inizia da (1,1) e sia lineare).
    :param genome: Il genoma da riparare (lista di tuple).
    :param goal: La posizione dell'obiettivo (tuple).
    :return: Il genoma riparato.
    """
    repaired_genome = [genome[0]]  # Inizia dalla prima posizione
    for coord in genome[1:]:
        # Controlla se la posizione corrente è valida rispetto all'ultima valida
        if manhattan_distance(repaired_genome[-1], coord) == 1:
            repaired_genome.append(coord)
        else:
            # Trova un percorso valido dalla posizione precedente
            repaired_genome = reconnect_path(repaired_genome, coord, grid)

    # Assicurati che l'obiettivo sia raggiunto alla fine del percorso
    if repaired_genome[-1] != goal:
        repaired_genome = reconnect_path(repaired_genome, goal, grid)

    return repaired_genome


def reconnect_path(path, target, grid ):
    """
    Riconnette il percorso a una posizione target creando un collegamento lineare.
    :param path: Il percorso corrente (lista di tuple).
    :param target: La posizione target (tuple).
    :return: Un percorso riconnesso.
    """
    current = path[-1]  # Posizione attuale
    while current != target:
        if current[0] < target[0] and grid.is_passable(current[0]):  # Spostati verso il basso
            current = (current[0] + 1, current[1])
        elif current[0] > target[0]:  # Spostati verso l'alto
            current = (current[0] - 1, current[1])
        elif current[1] < target[1]:  # Spostati verso destra
            current = (current[0], current[1] + 1)
        elif current[1] > target[1]:  # Spostati verso sinistra
            current = (current[0], current[1] - 1)

        path.append(current)

    return path

def manhattan_distance(coord1, coord2):
    """
    Calcola la distanza di Manhattan tra due coordinate.
    :param coord1: Prima coordinata (tuple).
    :param coord2: Seconda coordinata (tuple).
    :return: Distanza di Manhattan.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
