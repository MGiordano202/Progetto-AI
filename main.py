import pygame
from bomberman import BombermanGame

def main():
    pygame.init()
    game = BombermanGame(rows = 20, cols = 20, cell_size = 30)
    game.run()
    pygame.quit()



if __name__ == '__main__':
    main()