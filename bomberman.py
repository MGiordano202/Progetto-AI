import pygame
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
        self.manual_control = False  # Modalità di controllo (auto o manual)
        self.screen = pygame.display.set_mode((self.rows * self.cell_size, self.cols * self.cell_size))
        pygame.display.set_caption('Bomberman AI')


        # Griglia ed elementi
        self.grid = Grid(rows, cols)
        self.grid.generate_bomberman_map()
        self.player = Player(1, 1)
        self.pathfinder = Astar(self.grid)
        #self.enemies = [Enemy(rows - 2, cols - 2, self.pathfinder)]
        self.images = load_images(cell_size)
        self.bombs = []


        # Inizializzazione griglia
        self.grid.set_cell(self.player.row, self.player.col, "P")
        #for enemy in self.enemies:
            #self.grid.set_cell(enemy.row, enemy.col, "E")

        self.grid.set_cell(self.rows - 2,self.cols -2, "G")
        self.player_goal = (self.rows - 2,self.cols - 2)  # Obiettivo del giocatore

        self.ga = GeneticAlgorithm(
            grid = self.grid,
            player_start = (self.player.row, self.player.col),
            player_goal = self.player_goal,
            population_size = 50,
            generations = 100,
            mutation_rate = 0.1,
            tournament_size = 5
        )

        self.best_path = []
        self.current_step = 0

        # Esempio di muri (probabilmente da rimuovere)
    def add_walls(self):
        wall_positions = [(2, 2), (2, 3), (3, 2), (3, 3)]  # Example positions
        for row, col in wall_positions:
            self.grid.set_wall(row, col)



    def update(self):
        # Muove i nemici
        #for enemy in self.enemies:
            #old_row, old_col = enemy.row, enemy.col
            #enemy.update(self.grid)
            # Libera la cella precedente
            #self.grid.set_cell(old_row, old_col, 0)
            # Aggiorna la nuova posizione sulla griglia
            #self.grid.set_cell(enemy.row, enemy.col, "E")

        if (self.player.row, self.player.col) == self.player_goal:
            print("Obiettivo raggiunto! Hai vinto!")
            self.running = False
            return

        if not self.manual_control:
            if any(bomb.row == self.player.row and bomb.col == self.player.col for bomb in self.bombs):
                print("Aspettando la distruzione del blocco")
                self.update_bombs()
                return

            # A-Star
            #self.player.move_towards_goal(self.grid, self.pathfinder, self.player_goal, self.bombs)

            # Genetic Algorithm
            if self.best_path or self.current_step < len(self.best_path):
                action = self.best_path[self.current_step]
                self.execute_action(action)
                self.current_step += 1
            else:
                # Calcola il percorso con l'algoritmo genetico
                best_individual = self.ga.run()
                self.best_path = best_individual.path
                self.current_step = 0

                if not self.best_path:
                    print("Nessun percorso trovato.")
                    self.running = False
                    return

        # Gestione delle bombe
        self.update_bombs()

    def execute_action(self, action):
        """
        Esegue un'azione (movimento o piazzamento di una bomba).
        """
        if action == 'u':
            self.move_player(-1, 0)
        elif action == 'd':
            self.move_player(1, 0)
        elif action == 'l':
            self.move_player(0, -1)
        elif action == 'r':
            self.move_player(0, 1)
        elif action == 'b':
            self.bombs.append(self.player.place_bomb(self.grid, self.bombs))

    def update_bombs(self):
        for bomb in self.bombs[:]:
            if bomb is None:
                continue

            if bomb.has_exploded():
                print(f"Bomba esplosa in posizione: ({bomb.row}, {bomb.col})")
                bomb.explode(self.grid)
                self.bombs.remove(bomb)


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
                        self.bombs.append(self.player.place_bomb(self.grid, self.bombs))


    def move_player(self, d_row, d_col):
        new_row = self.player.row + d_row
        new_col = self.player.col + d_col

        if (0 <= new_row < self.rows and 0 <= new_col < self.cols and
                self.grid.is_passable(new_row, new_col)):
            # Aggiorna la posizione del giocatore
            if any(bomb.row == self.player.row and bomb.col == self.player.col for bomb in self.bombs):
                # Mantieni visivamente la bomba
                self.grid.set_cell(self.player.row, self.player.col, "B")
            else:
                # Ripristina la cella precedente
                self.grid.set_cell(self.player.row, self.player.col, "0")
            self.player.row, self.player.col = new_row, new_col
            self.grid.set_cell(self.player.row, self.player.col, "P")

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
            self.clock.tick(60)
