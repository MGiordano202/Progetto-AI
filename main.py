import pygame
from bomberman import BombermanGame

def main():
    pygame.init()
    game = BombermanGame(row = 13, cols = 15, cell_size = 50)
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()