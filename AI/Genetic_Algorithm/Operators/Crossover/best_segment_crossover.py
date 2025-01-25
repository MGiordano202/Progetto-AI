from AI.Genetic_Algorithm.individual import Individual


def best_segment_crossover(parent1, parent2, goal):
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
    child1_genome = []
    child2_genome = []

    for seg1, seg2 in zip(segments1, segments2):
        fitness_seg1 = sum(manhattan_distance(coord, goal) for coord in seg1)
        fitness_seg2 = sum(manhattan_distance(coord, goal) for coord in seg2)

        if fitness_seg1 < fitness_seg2:  # Se il segmento 1 è migliore
            child1_genome.extend(seg1)
            child2_genome.extend(seg2)
        else:                            # Se il segmento 2 è migliore
            child1_genome.extend(seg2)
            child2_genome.extend(seg1)

    child1 = Individual(child1_genome)
    child2 = Individual(child2_genome)

    return child1, child2


def manhattan_distance(coord1, coord2):
    """
    Calcola la distanza di Manhattan tra due coordinate.
    :param coord1: Prima coordinata (tuple).
    :param coord2: Seconda coordinata (tuple).
    :return: Distanza di Manhattan.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
