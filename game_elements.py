import pygame

def loadImages(cell_size):
    images = {
        "empty": pygame.image.load("empty.png"),
        "player": pygame.image.load("player.png"),
        "enemy": pygame.image.load("enemy.png"),
        "bomb": pygame.image.load("bomb.png"),
        "wall": pygame.image.load("wall.png"),
    }

    for key in images:
        images[key] = pygame.transform.scale(images[key], (cell_size, cell_size))
        return images