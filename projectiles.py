import pygame
import random
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
        self.timeout = 6000


class RobotBullet(Projectile):
    def __init__(self):
        super().__init__(4, 4, 10, assets.red)
        self.damage = 5
        self.change_x = self.speed
        self.timeout = 6000


class RobotMissile(Projectile):
    def __init__(self):
        super().__init__(10, 6, 3, assets.red)
        self.damage = 20
        self.change_x = self.speed
        self.timeout = 6000

    def reset_timer(self):
        time = random.randrange(60, 210, 30)
        return time


class SpiderWeb(Projectile):
    def __init__(self):
        super().__init__(100, 40, 0, assets.white)
        self.image = assets.spider_web_image
        self.rect = self.image.get_rect()
        self.damage = 10
        self.change_x = 0
        self.timeout = 5
        self.origin_x = -70
        self.origin_y = -10

    def reset_timer(self):
        time = 20
        return time


class SpiderBlob(Projectile):
    def __init__(self):
        super().__init__(19, 8, 6, assets.white)
        self.image = assets.spider_blob_image
        self.rect = self.image.get_rect()
        self.change_x = self.speed
        self.damage = 0
        self.timeout = 6000
        self.origin_x = -22
        self.origin_y = 15

    def reset_timer(self):
        time = random.randrange(120, 240, 30)
        return time

