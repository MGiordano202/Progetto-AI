import pygame

from bomb import Bomb
from grid import Grid
from player import Player
from enemy import Enemy
from game_elements import load_images
from AI.a_star import Astar

class BombermanGame:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((self.rows * self.cell_size, self.cols * self.cell_size))
        pygame.display.set_caption('Bomberman AI')


        #Griglia ed elementi
        self.grid = Grid(rows, cols)
        self.player = Player(1, 1)
        self.pathfinder = Astar(self.grid)
        self.enemies = [Enemy(rows - 2, cols - 2, self.pathfinder)]
        self.images = load_images(cell_size)
        self.bombs =[]


        #Inizializzazione griglia
        self.grid.set_cell(self.player.row, self.player.col, "P")
        for enemy in self.enemies:
            self.grid.set_cell(enemy.row, enemy.col, "E")

        #Inizializzazione muri
        self.add_walls()

        self.player_goal = (rows - 1, cols - 1)# Obiettivo del giocatore

    def add_walls(self):
        wall_positions = [(2, 2), (2, 3), (3, 2), (3, 3)]  # Example positions
        for row, col in wall_positions:
            self.grid.set_wall(row, col)



    def update(self):
        # Muove i nemici
        for enemy in self.enemies:
            old_row, old_col = enemy.row, enemy.col
            enemy.update(self.grid)
            # Libera la cella precedente
            self.grid.set_cell(old_row, old_col, 0)
            # Aggiorna la nuova posizione sulla griglia
            self.grid.set_cell(enemy.row, enemy.col, "E")

        self.player.move_towards_goal(self.grid, self.pathfinder, self.player_goal)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()
            self.grid.print_debug()
            self.clock.tick(30)
