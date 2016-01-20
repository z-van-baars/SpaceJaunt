import pygame


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
done = False

clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

key = (255, 0, 128)

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

shootman = pygame.image.load("art/shoot-man.png").convert()
stars = pygame.image.load("art/stars_64.png").convert()
crosshair_sheet = pygame.image.load("art/crosshair.png").convert()


jumpsound = pygame.mixer.Sound("sound/player/jump.wav")
pistol_shot_sound = pygame.mixer.Sound("sound/pistol_shot_2.wav")
spider_death_sound = pygame.mixer.Sound("sound/spider_death.wav")
empty_sound = pygame.mixer.Sound("sound/no_bullets.wav")
missile_fire = pygame.mixer.Sound("sound/fire_missile.wav")
player_hit_sound = pygame.mixer.Sound("sound/player_hit.wav")
game_over_sound = pygame.mixer.Sound("sound/game_over.wav")
webbed_sound = pygame.mixer.Sound("sound/webbed_sound.wav")
web_shoot_sound = pygame.mixer.Sound("sound/web_shoot.wav")
blob_shoot_sound = pygame.mixer.Sound("sound/blob_shoot.wav")

floor_image = pygame.image.load("art/floor_64.png")
spider_web_image = pygame.image.load("art/spider_web.png")
spider_blob_image = pygame.image.load('art/spider_blob.png')
spider_blob_image.set_colorkey(key)
spider_web_image.set_colorkey(key)

shootman.set_colorkey(key)

menu_font = pygame.font.SysFont('Arial', 20, True, False)
