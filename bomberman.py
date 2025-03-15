import pygame

from AI.ucs import UCS
from bomb import Bomb
from grid import Grid
from player import Player
from game_elements import load_images
from AI.a_star import Astar
from AI.Genetic_Algorithm.genetic_algorithm import GeneticAlgorithm

class BombermanGame:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.clock = pygame.time.Clock()
        self.running = True
        self.manual_control = False # Modalità di controllo (auto o manual)
        self.waiting_for_bomb = False  # Indica se il giocatore è in attesa dell'esplosione di una bomba
        self.screen = pygame.display.set_mode((self.rows * self.cell_size, self.cols * self.cell_size))
        pygame.display.set_caption('Bomberman AI')


        # Griglia ed elementi
        self.grid = Grid(rows, cols)
        self.grid.generate_bomberman_map()
        self.player = Player(1, 1)
        self.pathfinder = Astar(self.grid)
        
        self.images = load_images(cell_size)
        self.bombs = []


        # Inizializzazione griglia
        self.grid.set_cell(self.player.row, self.player.col, "P")
        self.grid.set_cell(self.rows - 2,self.cols -2, "G")
        self.goal = (self.rows - 2,self.cols - 2)  # Obiettivo del giocatore

        self.ga = GeneticAlgorithm(
            grid = self.grid,
            player_start = (self.player.row, self.player.col),
            player_goal = self.goal,
            population_size = 30,
            generations = 100,
            mutation_rate = 15,
            tournament_size = 5,
            crossover_rate = 0.8
        )

        self.best_path = []
        self.current_step = 0



    def update(self):

        if (self.player.row, self.player.col) == self.goal:
            print("Obiettivo raggiunto! Hai vinto!")
            self.running = False
            return



        if not self.manual_control:
            if self.waiting_for_bomb:  # Controlla se il giocatore è in attesa
                print("Aspettando l'esplosione della bomba...")
                self.update_bombs()  # Aggiorna lo stato delle bombe
                if not any(not bomb.has_exploded() for bomb in self.bombs):  # Controlla se tutte le bombe sono esplose
                    self.waiting_for_bomb = False  # Sblocca il giocatore
                return

            # Algoritmo A* / UCS
            #self.player.move_towards_goal(self.grid, self.pathfinder, self.goal, self.bombs)

            # Genetic Algorithm

            if self.current_step < len(self.best_path):
                action = self.best_path[self.current_step]
                self.execute_action(action)
                self.current_step += 1
            else:
                # Calcola il percorso con l'algoritmo genetico
                best_individual = self.ga.run()
                if best_individual and best_individual.genome:
                    self.best_path = best_individual.genome
                    self.current_step = 0

                if not self.best_path:
                    print("Nessun percorso trovato.")
                    self.running = False
                    return

        # Gestione delle bombe
        self.update_bombs()

    def execute_action(self, action):
        """
        Esegue un'azione specificata dall'algoritmo genetico.
        L'azione è una tupla (nuova_riga, nuova_colonna) che rappresenta la prossima posizione.
        """
        if self.waiting_for_bomb:
            print("Il giocatore sta aspettando che la bomba esploda.")
            return

        # Calcola lo spostamento necessario per raggiungere la nuova posizione
        new_row, new_col = action
        d_row = new_row - self.player.row
        d_col = new_col - self.player.col

        print(f"Eseguendo azione: spostamento verso ({new_row}, {new_col}) con d_row={d_row}, d_col={d_col}")  # Debug

        # Verifica se il movimento è valido
        self.move_player(d_row, d_col)

    def update_bombs(self):
        self.bombs = [bomb for bomb in self.bombs if bomb is not None]

        for bomb in self.bombs[:]:
            if bomb is None:
                continue

            if bomb.update(self.grid):
                print(f"Bomba esplosa in posizione: ({bomb.row}, {bomb.col})")
                self.bombs.remove(bomb)

        # Controlla se ci sono ancora bombe attive
        if not any(not bomb.has_exploded() for bomb in self.bombs):
            self.waiting_for_bomb = False



    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Premendo 'M' si cambia modalità
                    self.manual_control = not self.manual_control
                    self.best_path = None  # Resetta il percorso migliore
                    self.current_step = 0
                    print(f"Modalità {'manuale' if self.manual_control else 'automatica'} attivata.")

                if self.manual_control:  # Gestisci i movimenti manuali
                    if event.key == pygame.K_w:
                        self.move_player(-1, 0)
                    elif event.key == pygame.K_s:
                        self.move_player(1, 0)
                    elif event.key == pygame.K_a:
                        self.move_player(0, -1)
                    elif event.key == pygame.K_d:
                        self.move_player(0, 1)
                    elif event.key == pygame.K_SPACE:  # Spazio per piazzare una bomba
                        self.handle_bomb_placement()


    def move_player(self, d_row, d_col):
        if self.waiting_for_bomb:
            return

        new_row = self.player.row + d_row
        new_col = self.player.col + d_col

        if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.grid.is_passable(new_row, new_col):
            target_cell = self.grid.get_cell(new_row, new_col)

            if target_cell == "D":
                self.handle_bomb_placement()
                return


            # Aggiorna la posizione del giocatore
            if any(bomb.row == self.player.row and bomb.col == self.player.col for bomb in self.bombs):
                # Mantieni visivamente la bomba
                self.grid.set_cell(self.player.row, self.player.col, "B")
            else:
                # Ripristina la cella precedente
                self.grid.set_cell(self.player.row, self.player.col, "0")
            self.player.row, self.player.col = new_row, new_col
            self.grid.set_cell(self.player.row, self.player.col, "P")

    def handle_bomb_placement(self):
        """
        Gestisce il posizionamento di una nuova bomba nella posizione corrente del giocatore.
        Verifica che non ci sia già una bomba nella cella e che il giocatore non sia in attesa di un'esplosione.
        """
        # Se il giocatore è già in attesa, non è possibile piazzare una nuova bomba.
        if self.waiting_for_bomb:
            print("Il giocatore sta già aspettando che la bomba esploda!")
            return

        # Recupera la posizione corrente del giocatore.
        row, col = self.player.row, self.player.col

        # Verifica se in quella cella è già presente una bomba.
        for bomb in self.bombs:
            if bomb.row == row and bomb.col == col:
                print("C'è già una bomba in questa posizione!")
                return

        # Crea una nuova bomba e aggiorna la griglia.
        bomb = Bomb(row, col)
        self.grid.set_cell(row, col, "B")
        self.bombs.append(bomb)
        self.waiting_for_bomb = True
        print(f"Bomba piazzata in posizione ({row}, {col}).")

    def draw(self):
        self.screen.fill((0, 110, 0))
        self.grid.print_grid(self.screen, self.images, self.cell_size)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid.is_wall(row, col):
                    self.screen.blit(self.images["W"], (col * self.cell_size, row * self.cell_size))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            # Debug per il percorso dell'algoritmo genetico
            if self.best_path:
                print(f"Passo attuale: {self.current_step}/{len(self.best_path)}")

            self.grid.print_debug()
            self.clock.tick(5)
