import pygame
from bomberman import BombermanGame

def main():
    pygame.init()
    game = BombermanGame(rows = 11, cols = 11, cell_size = 32)
    game.run()
    pygame.quit()



if __name__ == '__main__':
    main()