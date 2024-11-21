import pygame
import random
from constants import *

class Ship:
    """Base class for ships."""
    def __init__(self, x, y, width, height, image, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.vel = vel

    def draw(self, window):
        """Draw the ship on the screen."""
        window.blit(self.image, (self.x, self.y))

    def move(self):
        """Move the ship."""
        self.y += self.vel

    def get_rect(self):
        """Get the rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class FlyShip(Ship):
    """Subclass for fly ships."""
    def __init__(self, x, y, vel, level):
        width, height = 60, 80  
        super().__init__(x, y, width, height, FLY_IMAGE, vel + random.uniform(0, ENEMY_VEL_RANDOMNESS * level))

    def move(self):
        """Customize movement if needed."""
        super().move()


class BumblebeeShip(Ship):
    """Subclass for bumblebee ships."""
    def __init__(self, x, y, vel, level):
        width, height = 40, 40  
        super().__init__(x, y, width, height, BUMBLEBEE_IMAGE, vel + random.uniform(0, ENEMY_VEL_RANDOMNESS * level))
        self.health = 2  


class WaspShip(Ship):
    """Subclass for wasp ships."""
    def __init__(self, x, y, vel, level):
        width, height = 50, 50  
        super().__init__(x, y, width, height, WASP_IMAGE, vel + random.uniform(0, ENEMY_VEL_RANDOMNESS * level))
        self.health = 3  
        self.projectiles = []  
        self.last_shot_time = 0 

    def shoot(self):
        """Shoot a missile as a projectile."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000:  
            proj_rect = pygame.Rect(self.x + self.width // 2 - 10, self.y + self.height, 20, 40) 
            self.projectiles.append(proj_rect)
            self.last_shot_time = current_time

    def move_projectiles(self):
        """Move projectiles downward."""
        for proj in self.projectiles[:]:
            proj.y += PROJECTILE_VEL  
            if proj.y > HEIGHT:
                self.projectiles.remove(proj)

    def draw(self, window):
        """Draw the WaspShip and its projectiles."""
        super().draw(window)  
        for proj in self.projectiles:
            window.blit(MISSILE_IMAGE, (proj.x, proj.y))
