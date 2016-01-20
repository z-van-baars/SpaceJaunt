import assets
import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(assets.green)
        self.rect = self.image.get_rect()


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
