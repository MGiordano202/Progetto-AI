import pygame
from bomberman import BombermanGame

def main():
    pygame.init()
    game = BombermanGame(rows = 9, cols = 9, cell_size = 32)
    game.run()
    pygame.quit()



if __name__ == '__main__':
    main()