import pygame
from grid import Grid
from player import Player
from enemy import Enemy
from game_elements import loadImages

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
        self.enemies = [Enemy(rows - 2, cols - 2)]
        self.images = loadImages(cell_size)

        #Inizializzazione griglia
        self.grid.setCell(self.player.row, self.player.col, "player")
        for enemy in self.enemies:
            self.grid.setCell(enemy.row, enemy.col, "enemy")


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move("up", self.grid)
                elif event.key == pygame.K_DOWN:
                    self.player.move("down", self.grid)
                elif event.key == pygame.K_LEFT:
                    self.player.move("left", self.grid)
                elif event.key == pygame.K_RIGHT:
                    self.player.move("right", self.grid)
                elif event.key == pygame.K_SPACE:
                    self.player.place_bomb(self.grid)

    def update(self):
        # Muove i nemici
        for enemy in self.enemies:
            old_row, old_col = enemy.row, enemy.col
            enemy.move(self.grid)
            # Libera la cella precedente
            self.grid.setCell(old_row, old_col, "empty")
            # Aggiorna la nuova posizione sulla griglia
            self.grid.setCell(enemy.row, enemy.col, "enemy")

    def draw(self):
        self.screen.fill((0, 110, 0))
        self.grid.print_grid(self.screen, self.images, self.cell_size)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.grid.print_debug()
            self.clock.tick(30)
