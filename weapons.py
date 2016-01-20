import pygame
import projectiles
import utilities
import assets


class Weapon():
    def __init__(self):
        self.projectile = None
        self.rate_of_fire = None
        self.accuracy = None
        self.ammo_type = None
        self.current_ammo = None
        self.mag_size = None
        self.current_mag = None
        self.automatic = False
        self.loaded = True
        self.empty_sound = assets.empty_sound

    def fire(self, current_level, pos, player_x, player_y, player):
        origin_modifier = {6: (30, -10), 5: (55, 5), 4: (55, 15), 3: (60, 20), 2: (50, 30), 1: (45, 40), 0: (10, 60)}
        new_projectile = projectiles.Bullet()
        vector_mod = origin_modifier[player.arm_state]
        new_projectile.rect.x = player_x + vector_mod[0]
        new_projectile.rect.y = player_y + vector_mod[1]
        x = pos[0] + 15
        y = pos[1] + 15
        if pos[0] < player_x + 65:
            x = player_x + 65
        assets.pistol_shot_sound.play()
        vector = utilities.get_vector(new_projectile, x, y, new_projectile.rect.x, new_projectile.rect.y)
        new_projectile.change_x = vector[0]
        new_projectile.change_y = vector[1]
        current_level.projectiles_list.add(new_projectile)
        player.firing = self.automatic
        self.current_mag -= 1
        if self.current_mag == 0:
            self.loaded = False


class Pistol(Weapon):
    def __init__(self):
        super().__init__()
        self.projectile_type = type(projectiles.Bullet)
        self.automatic = False
        self.mag_size = 10
        self.current_mag = 10
        self.current_ammo = 1000


pistol = Pistol()

weapons = [pistol]