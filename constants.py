import pygame

pygame.font.init()

# Screen dimensions
WIDTH, HEIGHT = 1500, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Images 
IMG_FOLDER = "img/"
BG = pygame.transform.scale(pygame.image.load(f"{IMG_FOLDER}bg.jpeg"), (WIDTH, HEIGHT))
SHIP_IMAGE = pygame.transform.scale(pygame.image.load(f"{IMG_FOLDER}ship.png"), (120, 120))
PROJ_IMAGE = pygame.transform.scale(pygame.image.load(f"{IMG_FOLDER}proj.png"), (30, 80))
FLY_IMAGE = pygame.transform.scale(pygame.image.load(f"{IMG_FOLDER}fly.png"), (60, 80))
BUMBLEBEE_IMAGE = pygame.transform.scale(pygame.image.load(f"{IMG_FOLDER}bumblebee.png"), (40, 40))
WASP_IMAGE = pygame.transform.scale(pygame.image.load(f"{IMG_FOLDER}wasp.png"), (50, 50))
MISSILE_IMAGE = pygame.transform.scale(pygame.image.load(f"{IMG_FOLDER}missile.png"), (20, 40))

# Player and game settings
PLAYER_SIZE = 60
PLAYER_VEL = 6
BASE_ENEMY_VEL = 4
ENEMY_VEL_INCREMENT = 1
ENEMY_VEL_RANDOMNESS = 2
BASE_ENEMY_ADD_INCREMENT = 2000
ENEMY_ADD_DECREMENT = 200
PROJECTILE_VEL = 10
FIRE_COOLDOWN = 250
LIVES = 3

# Font
FONT = pygame.font.SysFont("comicsans", 30)
