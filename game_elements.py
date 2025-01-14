import pygame

def load_images(cell_size):
    images = {
        "0": pygame.image.load("img/empty.png"),
        "P": pygame.image.load("img/player.png"),
        "E": pygame.image.load("img/enemy.png"),
        "B": pygame.image.load("img/bomb.png"),
        "W": pygame.image.load("img/wall.png"),
        "D": pygame.image.load("img/wooden_box.png"),
        "G": pygame.image.load("img/doors.png"),
    }

    for key in images:
        images[key] = pygame.transform.scale(images[key], (cell_size, cell_size))
    return images