from AI.Genetic_Algorithm.Operators.Crossover.best_segment_crossover import repair_genome

from grid import Grid

# Configura la griglia (modifica secondo la tua configurazione)
grid = Grid(rows=10, cols=10)
# Assicurati che la griglia sia coerente con ciò che ti serve per il test (es. posizioni passabili, ostacoli, ecc.)

# Definisci lo start e il goal
start = (0, 0)
goal = (5, 5)

# Crea un percorso “rotto”: ad esempio, un percorso in cui viene inserito un salto non valido
broken_genome = [start, (0, 1), (0, 3), (1, 3), (2, 3), goal]

# Stampa il percorso originale
print("Percorso originale:", broken_genome)

# Esegui la riparazione
repaired_genome = repair_genome(broken_genome, goal, grid)

print("Percorso riparato:", repaired_genome)
