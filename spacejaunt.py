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


def lose(lost):
    global assets
    assets.game_over_sound.play()
    game_over_stamp = assets.menu_font.render("GAME OVER", True, assets.green)
    play_again_stamp = assets.menu_font.render("PLAY AGAIN? Y / N", True, assets.green)
    while lost:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lost = False
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    lost = False
                    done = True
                if event.key == pygame.K_y:
                    lost = False
                    done = False

        assets.screen.blit(game_over_stamp, [330, 250])
        assets.screen.blit(play_again_stamp, [300, 300])
        pygame.display.flip()
        assets.clock.tick(60)
    return done


def reset_game(player_object, level_01_object):
    pygame.mouse.set_visible(0)

    moving_objects = pygame.sprite.Group()

    level_01 = level_01_object
    level_list = [level_01, level_01]
    level = 0
    current_level = level_list[level]

    player_char = player_object
    player_char.current_level = current_level

    crosshairs = Crosshair()
    moving_objects.add(crosshairs)
    moving_objects.add(player_char)

    health_bar = pygame.sprite.Sprite()
    done = False
    lost = False

    return level_list, player_char, moving_objects, crosshairs, health_bar, done, lost, current_level


def main(assets, utilities, player, levels, enemy):
    level_list, player_char, moving_objects, crosshairs, health_bar, done, lost, current_level = reset_game(player.Player(), levels.Level_01())

    paused_stamp = assets.menu_font.render("PAUSED press 'P' to Resume", True, assets.red)

    while not done:
        ammo_stamp = assets.menu_font.render(str(player_char.weapon.current_ammo), False, assets.white)
        mag_stamp = assets.menu_font.render(str(player_char.weapon.current_mag), False, assets.green)

        pos = pygame.mouse.get_pos()
        crosshairs.rect.x = pos[0]
        crosshairs.rect.y = pos[1]
        crosshairs.get_state(current_level, player_char, pos)

        health_bar.image = pygame.Surface([player_char.health, 20])
        health_bar.image.fill(assets.green)
        health_bar.rect = health_bar.image.get_rect()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                lost = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_char.change_x = -player_char.speed
                if event.key == pygame.K_d:
                    player_char.change_x = player_char.speed
                if event.key == pygame.K_SPACE:
                    player_char.jump()
                if event.key == pygame.K_r:
                    player_char.reload()
                if event.key == pygame.K_RETURN:
                    new_spider = enemy.Robot()
                    new_spider.rect.x = 600
                    new_spider.rect.y = 535
                    current_level.enemy_list.add(new_spider)
                if event.key == pygame.K_p:
                    paused = True
                    assets.screen.blit(paused_stamp, [260, 250])
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                paused = False
                                done = True
                                lost = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    paused = False
                        pygame.display.flip()
                        assets.clock.tick(60)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player_char.change_x = 0
                if event.key == pygame.K_d:
                    player_char.change_x = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                player_char.firing = True

            elif event.type == pygame.MOUSEBUTTONUP:
                player_char.firing = False

        player_char.update(pos)

        if player_char.rect.right >= 300:
            diff = player_char.rect.right - 300
            player_char.rect.right = 300
            current_level.shift_world(-diff, player_char)

        if player_char.rect.left <= 120:
            diff = 120 - player_char.rect.left
            player_char.rect.left = 120
            current_level.shift_world(diff, player_char)

        current_level.update(assets.screen, assets.screen_width, assets.screen_height, player_char)

        current_level.draw(assets.screen)
        moving_objects.draw(assets.screen)
        assets.screen.blit(ammo_stamp, [100, 5])
        assets.screen.blit(mag_stamp, [150, 5])
        assets.screen.blit(health_bar.image, [61, 30])
        assets.screen.blit(player_char.arm_images[player_char.arm_state], [player_char.rect.x - 2, player_char.rect.y - 12])

        if player_char.health < 1:
            lost = True
            done = lose(lost)
            if not done:
                level_list, player_char, moving_objects, crosshairs, health_bar, done, lost, current_level = reset_game(player.Player(), levels.Level_01())

        pygame.display.flip()
        assets.clock.tick(60)

main(assets, utilities, player, levels, enemy)


pygame.quit()
