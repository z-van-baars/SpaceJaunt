import pygame
import assets


class Projectile(pygame.sprite.Sprite):
    def __init__(self, width, height, speed, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.change_x = 0
        self.change_y = 0
        self.damage = 0


class Bullet(Projectile):
    def __init__(self):
        super().__init__(4, 4, 20, assets.green)
        self.damage = 10


class RobotBullet(Projectile):
    def __init__(self):
        super().__init__(4, 4, 10, assets.red)
        self.damage = 5
        self.change_x = self.speed


class RobotMissile(Projectile):
    def __init__(self):
        super().__init__(10, 6, 3, assets.red)
        self.damage = 20
        self.change_x = self.speed

