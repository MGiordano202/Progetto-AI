import pygame

def loadImages(cell_size):
    images = {
        "empty": pygame.image.load("img/empty.png"),
        "player": pygame.image.load("img/player.png"),
        "enemy": pygame.image.load("img/enemy.png"),
        "bomb": pygame.image.load("img/bomb.png"),
        "wall": pygame.image.load("img/wall.png"),
    }

    for key in images:
        images[key] = pygame.transform.scale(images[key], (cell_size, cell_size))
        return images