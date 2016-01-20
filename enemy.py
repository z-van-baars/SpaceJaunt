import pygame
import assets
import random
import projectiles
from spritesheet import Spritesheet


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= (assets.screen_height - 80) - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = (assets.screen_height - 80) - self.rect.height

    def collide(self, current_level):

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, current_level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def move(self):

        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def death(self):
        if not self.dead:
            self.death_sound.play()
            self.dead = True
            self.frame = 0
            self.change_x = 0
            self.change_y = 0
        self.frame += 1
        self.image = self.death_frames[self.frame]
        if self.frame > (len(self.death_frames) - 2):
            self.kill()


class Spider(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 30
        self.speed = 1
        self.change_x = 0
        self.change_y = 1
        self.frame = 0
        self.dead = False
        self.death_sound = assets.spider_death_sound

        self.walking_frames = []
        self.death_frames = []

        sprite_sheet = Spritesheet("art/spider_sheet.png")
        image = sprite_sheet.get_image(0, 0, 90, 45)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        image = sprite_sheet.get_image(90, 0, 90, 45)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        image = sprite_sheet.get_image(0, 0, 90, 45)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        image = sprite_sheet.get_image(180, 0, 90, 45)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        sprite_sheet = Spritesheet("art/spider_death_sheet.png")
        image = sprite_sheet.get_image(0, 0, 105, 90)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(105, 0, 105, 90)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(210, 0, 105, 90)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        self.image = self.walking_frames[self.frame]
        self.rect = self.image.get_rect()

    def update(self, player, world_shift, current_level):
        if self.health > 0:
            if player.rect.x + world_shift < self.rect.x + 100:
                self.change_x = -self.speed
            elif player.rect.x + world_shift == self.rect.x:
                self.change_x = 0
            else:
                self.change_x = 0
            self.get_frame()
        else:
            self.death()

        self.calc_grav()
        self.move()
        self.collide(current_level)

    def get_frame(self):
        if self.change_x > 0 or self.change_x < 0:
            self.frame += 1
        else:
            self.frame = 0
        if self.frame > 23:
            self.frame = 0
        self.image = self.walking_frames[self.frame]


class Robot(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 80
        self.speed = 0.1
        self.change_x = 0
        self.change_y = 1
        self.frame = 0
        self.dead = False
        self.death_sound = assets.spider_death_sound
        self.shoot_timer = 60

        self.walking_frames = []
        self.death_frames = []

        sprite_sheet = Spritesheet("art/robot_sheet.png")
        image = sprite_sheet.get_image(0, 0, 45, 47)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        image = sprite_sheet.get_image(45, 0, 45, 47)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        image = sprite_sheet.get_image(0, 0, 45, 47)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        image = sprite_sheet.get_image(135, 0, 45, 47)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)
        self.walking_frames.append(image)

        sprite_sheet = Spritesheet("art/robot_death_sheet.png")
        image = sprite_sheet.get_image(0, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(50, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(100, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(150, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(200, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(250, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(300, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)

        image = sprite_sheet.get_image(350, 0, 50, 60)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)
        self.death_frames.append(image)


        self.image = self.walking_frames[self.frame]
        self.rect = self.image.get_rect()

    def update(self, player, world_shift, current_level):
        if self.health > 0:
            if player.rect.x > self.rect.x - 800 and player.rect.x < self.rect.x - 200:
                self.change_x = -self.speed
            if player.rect.x > self.rect.x - 800:
                self.shoot(player, current_level)
                if player.rect.x > self.rect.x - 150:
                    self.change_x = 0
            self.get_frame()
        else:
            self.death()

        self.calc_grav()
        self.move()
        self.collide(current_level)

    def shoot(self, player, current_level):
        print(self.shoot_timer)
        self.shoot_timer -= 1
        if self.shoot_timer == 0:
            self.shoot_timer = random.randrange(90, 210, 30)
            new_missile = projectiles.RobotMissile()
            new_missile.rect.x = self.rect.x
            new_missile.rect.y = self.rect.y + 20
            current_level.enemy_projectiles_list.add(new_missile)
            assets.missile_fire.play()

    def get_frame(self):
        if self.change_x > 0 or self.change_x < 0:
            self.frame += 1
        else:
            self.frame = 0
        if self.frame > 23:
            self.frame = 0
        self.image = self.walking_frames[self.frame]


