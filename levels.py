import pygame
import assets
import platforms
import enemy
import random
from projectiles import SpiderBlob


class Level():
    def __init__(self):
        self.background = None
        self.world_shift = 0
        self.projectiles_list = pygame.sprite.Group()
        self.enemy_projectiles_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()

    def update(self, screen, screen_width, screen_height, player):
        for each in self.projectiles_list:
            each.rect.x += each.change_x
            each.rect.y += each.change_y
            if each.rect.x > screen_width:
                self.projectiles_list.remove(each)
            hits = pygame.sprite.spritecollide(each, self.enemy_list, False)
            for hit in hits:
                hit.health -= each.damage
                self.projectiles_list.remove(each)
        for each in self.enemy_projectiles_list:
            each.rect.x -= each.change_x
            each.rect.y -= each.change_y
            each.timeout -= 1
            if each.timeout == 0 or each.rect.x < 0:
                self.enemy_projectiles_list.remove(each)
        hits = pygame.sprite.spritecollide(player, self.enemy_projectiles_list, False)
        for each in hits:
            player.health -= each.damage
            self.enemy_projectiles_list.remove(each)
            assets.player_hit_sound.play()
            if type(each) == type(SpiderBlob()) and player.webcounter == 0:
                print("you got webbed")
                player.webcounter = 90
                assets.webbed_sound.play()
        for foe in self.enemy_list:
            foe.update(player, self.world_shift, self)

    def draw(self, screen):

        screen.blit(self.background, [self.world_shift / 10, 0])
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.projectiles_list.draw(screen)
        self.enemy_projectiles_list.draw(screen)

    def shift_world(self, shift_x, player):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x
        if self.world_shift > 120:
            self.world_shift = 120
        elif self.world_shift < -(self.level_limit):
            self.world_shift = -(self.level_limit)
        else:
            for platform in self.platform_list:
                platform.rect.x += shift_x
            for each in self.enemy_list:
                each.rect.x += shift_x
            for each in self.projectiles_list:
                each.rect.x += shift_x
            for each in self.enemy_projectiles_list:
                each.rect.x += shift_x


class Level_01(Level):
    def __init__(self):
        super().__init__()
        self.background = assets.stars
        self.level_limit = 11800

        level = [[210, 30, 300, 405],
                 [210, 30, 700, 413],
                 ]

        spiders = []
        robots = []
        # for x in range(30):
            # random_x = random.randint(800, 11600)
            # spiders.append((random_x, 535))
        # for x in range(30):
            # random_x = random.randint(800, 11600)
            # robots.append((random_x, 535))
        for each in spiders:
            new_spider = enemy.Spider()
            new_spider.rect.x = each[0]
            new_spider.rect.y = each[1]
            self.enemy_list.add(new_spider)
        for each in robots:
            new_robot = enemy.Robot()
            new_robot.rect.x = each[0]
            new_robot.rect.y = each[1]
            self.enemy_list.add(new_robot)

        for platform in level:
            block = platforms.Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)
        floor = platforms.Floor()
        floor.image = assets.floor_image
        floor.rect = floor.image.get_rect()
        floor.rect.x = -120
        floor.rect.y = 520
        self.platform_list.add(floor)
        floor = platforms.Floor()
        floor.image = assets.floor_image
        floor.rect = floor.image.get_rect()
        floor.rect.x = 6280
        floor.rect.y = 520
        self.platform_list.add(floor)

