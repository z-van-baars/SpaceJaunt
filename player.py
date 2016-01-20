import pygame
import utilities
import weapons
import assets
from spritesheet import Spritesheet
import math


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.change_x = 0
        self.change_y = 0
        self.current_level = None
        self.weapon_list = []
        self.current_weapon = 0
        self.weapon = None
        self.speed = 5
        self.face = 'R'
        self.frame = 0
        self.firing = False
        self.max_health = 100
        self.health = 100
        self.arm_state = 3
        self.webcounter = 0
        self.crouched = False
        self.try_stand = False

        pistol = weapons.Pistol()
        self.weapon_list.append(pistol)

        self.weapon = self.weapon_list[self.current_weapon]

        self.arm_images = []
        sprite_sheet = Spritesheet("art/shootman_arms.png")
        image = sprite_sheet.get_image(0, 0, 65, 72)
        self.arm_images.append(image)
        image = sprite_sheet.get_image(65, 0, 65, 72)
        self.arm_images.append(image)
        image = sprite_sheet.get_image(130, 0, 65, 72)
        self.arm_images.append(image)
        image = sprite_sheet.get_image(195, 0, 65, 72)
        self.arm_images.append(image)
        image = sprite_sheet.get_image(260, 0, 65, 72)
        self.arm_images.append(image)
        image = sprite_sheet.get_image(325, 0, 65, 72)
        self.arm_images.append(image)
        image = sprite_sheet.get_image(390, 0, 65, 72)
        self.arm_images.append(image)

        sprite_sheet = Spritesheet("art/shootman_sheet.png")

        self.walking_frames_r = []

        image = sprite_sheet.get_image(10, 0, 50, 85)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(75, 0, 50, 85)
        for x in range(7):
            self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(140, 0, 50, 85)
        for x in range(7):
            self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(205, 0, 50, 85)
        for x in range(7):
            self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(140, 0, 50, 85)
        for x in range(7):
            self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(270, 0, 50, 85)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(335, 0, 50, 85)
        self.walking_frames_r.append(image)

        self.image = self.walking_frames_r[self.frame]

        self.crouched_frames_r = []

        image = sprite_sheet.get_image(10, 95, 50, 75)
        self.crouched_frames_r.append(image)
        image = sprite_sheet.get_image(75, 95, 50, 75)
        for x in range(7):
            self.crouched_frames_r.append(image)
        image = sprite_sheet.get_image(140, 95, 50, 75)
        for x in range(7):
            self.crouched_frames_r.append(image)
        image = sprite_sheet.get_image(205, 95, 50, 75)
        for x in range(7):
            self.crouched_frames_r.append(image)
        image = sprite_sheet.get_image(140, 95, 50, 75)
        for x in range(7):
            self.crouched_frames_r.append(image)
        image = sprite_sheet.get_image(10, 95, 50, 75)
        self.crouched_frames_r.append(image)

        self.rect = self.image.get_rect()

        self.rect.x = 120
        self.rect.y = 520

    def get_arm_state(self, pos):
        # distance_to_target = utilities.distance(pos[0] + 15, pos[1] + 15, self.rect.x, self.rect.y)
        x_dist = pos[0] + 15 - self.rect.x + 30
        y_dist = pos[1] + 15 - self.rect.y + 12
        y_dist = y_dist * -1
        if x_dist <= 0:
            x_dist = 1

        factor = y_dist / x_dist
        arm_angle = math.degrees(math.atan(factor))
        if arm_angle <= -60:
            self.arm_state = 0
        elif -35 >= arm_angle > -60:
            self.arm_state = 1
        elif -15 >= arm_angle > -35:
            self.arm_state = 2
        elif 15 > arm_angle > -15:
            self.arm_state = 3
        elif 35 > arm_angle >= 15:
            self.arm_state = 4
        elif 60 > arm_angle >= 35:
            self.arm_state = 5
        elif arm_angle >= 60:
            self.arm_state = 6

    def get_frame(self):
        old_x = self.rect.x
        old_y = self.rect.y
        if self.change_x == 0 and self.change_y == 0:
            self.frame = 0
        if self.change_y != 0:
            self.frame = 29
        elif self.change_x > 0:
            self.frame += 1
            if self.frame > 28:
                self.frame = 1
        elif self.change_x < 0:
            self.frame -= 1
            if self.frame < 1:
                self.frame = 28
        if self.webcounter > 0:
            self.change_x = 0
            self.change_y = 0
            self.frame = 30

        if self.crouched:
            self.image = self.crouched_frames_r[self.frame]
        else:
            self.image = self.walking_frames_r[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y

    def update(self, pos):
        if self.try_stand:
            self.uncrouch()
        self.get_arm_state(pos)
        if self.firing and self.webcounter == 0:
            self.shoot(pos)
        # Gravity
        self.calc_grav()
        if self.webcounter > 0:
            self.change_x = 0
            self.webcounter -= 1

        # Move left/right
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.current_level.platform_list, False)
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

        block_hit_list = pygame.sprite.spritecollide(self, self.current_level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        self.get_frame()

    def crouch(self):
        if not self.crouched:
            self.rect.y += 10
            self.crouched = True
            self.was_crouched = True

    def uncrouch(self):
        self.rect.y -= 10
        block_hit_list = pygame.sprite.spritecollide(self, self.current_level.platform_list, False)
        if block_hit_list:
            self.crouched = True
            self.rect.y += 10
        else:
            self.crouched = False
            self.try_stand = False

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= (assets.screen_height - 80) - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = (assets.screen_height - 80) - self.rect.height

    def reload(self):
        if self.weapon.current_ammo > 0:
            self.weapon.current_ammo += self.weapon.current_mag
            self.weapon.current_mag = 0
            self.weapon.current_mag = min(self.weapon.mag_size, self.weapon.current_ammo)
            self.weapon.current_ammo -= self.weapon.mag_size
            if self.weapon.current_ammo < 0:
                self.weapon.current_ammo = 0
            self.weapon.loaded = True

    def shoot(self, pos):
        if self.weapon.loaded:
            self.weapon.fire(self.current_level, pos, self.rect.x, self.rect.y, self)
        else:
            self.weapon.empty_sound.play()
            self.firing = False

    def jump(self):
        """ Called when user hits 'jump' button. """
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.current_level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= assets.screen_height - 80:
            assets.jumpsound.play()
            self.change_y = -10