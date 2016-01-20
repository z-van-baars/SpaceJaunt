import pygame
import utilities
import assets
import player
import levels
import enemy
from spritesheet import Spritesheet


pygame.display.set_caption("Time for a jaunt")


class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.state = 2

        sprite_sheet = Spritesheet("art/crosshair.png")

        self.states = []
        image = sprite_sheet.get_image(0, 0, 30, 30)
        self.states.append(image)
        image = sprite_sheet.get_image(0, 30, 30, 30)
        self.states.append(image)
        image = sprite_sheet.get_image(0, 60, 30, 30)
        self.states.append(image)

        self.image = self.states[self.state]

        self.rect = self.image.get_rect()

    def get_state(self, current_level, player, pos):
        if pos[0] < (player.rect.x + 30):
            self.state = 0
        else:
            self.state = 2
        self.image = self.states[self.state]


def update(player, level):
    player.rect.x += player.change_x
    player.rect.y += player.change_y


level_01 = levels.Level_01()
levels = [level_01, level_01]
level = 0

current_level = levels[level]

player = player.Player()
player.current_level = current_level

done = False
lost = True
pygame.mouse.set_visible(0)

moving_objects = pygame.sprite.Group()

crosshairs = Crosshair()
moving_objects.add(crosshairs)
moving_objects.add(player)

health_bar = pygame.sprite.Sprite()


while not done:
    ammo_stamp = assets.menu_font.render(str(player.weapon.current_ammo), False, assets.white)
    mag_stamp = assets.menu_font.render(str(player.weapon.current_mag), False, assets.green)

    pos = pygame.mouse.get_pos()
    crosshairs.rect.x = pos[0]
    crosshairs.rect.y = pos[1]
    crosshairs.get_state(current_level, player, pos)

    health_bar.image = pygame.Surface([player.health, 20])
    health_bar.image.fill(assets.green)
    health_bar.rect = health_bar.image.get_rect()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            lost = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.change_x = -player.speed
            if event.key == pygame.K_d:
                player.change_x = player.speed
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_r:
                player.reload()
            if event.key == pygame.K_RETURN:
                new_spider = enemy.Robot()
                new_spider.rect.x = 600
                new_spider.rect.y = 535
                current_level.enemy_list.add(new_spider)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.change_x = 0
            if event.key == pygame.K_d:
                player.change_x = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.firing = True

        elif event.type == pygame.MOUSEBUTTONUP:
            player.firing = False

    player.update(pos)

    if player.rect.right >= 300:
        diff = player.rect.right - 300
        player.rect.right = 300
        current_level.shift_world(-diff, player)

    if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff, player)

    current_level.update(assets.screen, assets.screen_width, assets.screen_height, player)

    current_level.draw(assets.screen)
    moving_objects.draw(assets.screen)
    assets.screen.blit(ammo_stamp, [100, 5])
    assets.screen.blit(mag_stamp, [150, 5])
    assets.screen.blit(health_bar.image, [61, 30])
    assets.screen.blit(player.arm_images[player.arm_state], [player.rect.x - 2, player.rect.y - 12])

    if player.health < 1:
        done = True
        assets.game_over_sound.play()

    pygame.display.flip()
    assets.clock.tick(60)

while lost:

    game_over_stamp = assets.menu_font.render("GAME OVER", True, assets.green)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lost = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                lost = False

    assets.screen.blit(game_over_stamp, [330, 250])
    pygame.display.flip()
    assets.clock.tick(60)

pygame.quit()
