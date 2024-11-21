import pygame
import time
import random
from ships import FlyShip, BumblebeeShip, WaspShip
from constants import *


def draw(player_x, player_y, elapsed_time, enemies, projectiles, lives, level, score):
    WIN.blit(BG, (0, 0))

    lives_text = FONT.render(f'Lives: {lives}', 1, "white")
    WIN.blit(lives_text, (200, 20))
    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, "white")
    WIN.blit(time_text, (20, 20))
    level_text = FONT.render(f'Level: {level}', 1, "white")
    WIN.blit(level_text, (WIDTH - 150, 20))
    score_text = FONT.render(f'Score: {score}', 1, "white")  
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 20))  

    WIN.blit(SHIP_IMAGE, (player_x - PLAYER_SIZE, player_y - PLAYER_SIZE))

    for proj in projectiles:
        WIN.blit(PROJ_IMAGE, (proj.x, proj.y))

    for enemy in enemies:
        enemy.draw(WIN)

    pygame.display.update()

def get_triangle_points(x, y, size):
    """Return the points of an upward-facing triangle centered at (x, y)."""
    half_size = size // 2
    return [(x, y - size), (x - half_size, y + half_size), (x + half_size, y + half_size),]

def triangle_collision(triangle_points, rect):
    """Approximate triangle-rectangle collision by checking if any triangle point is inside the rectangle."""
    for point in triangle_points:
        if rect.collidepoint(point):
            return True
    return False

def level_complete_message(level):
    WIN.blit(BG, (0, 0))
    level_complete_text = FONT.render(f"Level {level} Complete!", 1, "white")
    WIN.blit(level_complete_text, (WIDTH / 2 - level_complete_text.get_width() / 2, HEIGHT / 2))
    pygame.display.update()
    pygame.time.delay(3000)  

def game_loop(level, max_enemy_vel, max_add_increment, score):
    global LIVES
    player_x = WIDTH // 2
    player_y = HEIGHT - 100
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    enemy_add_increment = max(400, max_add_increment)
    enemy_count = 0
    enemies = []
    projectiles = []
    last_shot_time = 0

    num_enemies = min(3 + level, 5)
    enemy_vel_base = max_enemy_vel

    while True:
        enemy_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        player_points = get_triangle_points(player_x, player_y, PLAYER_SIZE)

        if enemy_count > random.randint(300, enemy_add_increment):
            for _ in range(num_enemies):
                enemy_x = random.randint(0, WIDTH - 80)

                bumblebee_spawn_chance = min(0.3 + (0.05 * level), 0.7)
                wasp_spawn_chance = min(0.2 + (0.03 * level), 0.5)

                rand_val = random.random()
                if rand_val < wasp_spawn_chance:
                    enemy = WaspShip(enemy_x, -100, enemy_vel_base, level)
                elif rand_val < wasp_spawn_chance + bumblebee_spawn_chance:
                    enemy = BumblebeeShip(enemy_x, -100, enemy_vel_base, level)
                else:
                    enemy = FlyShip(enemy_x, -80, enemy_vel_base, level)

                enemies.append(enemy)

            enemy_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", enemy_vel_base, max_add_increment, score

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - PLAYER_VEL - PLAYER_SIZE // 2 >= 0:
            player_x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player_x + PLAYER_VEL + PLAYER_SIZE // 2 <= WIDTH:
            player_x += PLAYER_VEL
        if keys[pygame.K_SPACE] and (pygame.time.get_ticks() - last_shot_time > FIRE_COOLDOWN):
            proj_rect = pygame.Rect(player_x - 10, player_y - PLAYER_SIZE, 10, 20)
            projectiles.append(proj_rect)
            last_shot_time = pygame.time.get_ticks()

        for proj in projectiles[:]:
            proj.y -= PROJECTILE_VEL
            if proj.y < -PROJ_IMAGE.get_height():
                projectiles.remove(proj)

        for enemy in enemies[:]:
            enemy.move()

            if isinstance(enemy, WaspShip):
                enemy.shoot()
                enemy.move_projectiles()

                for proj in enemy.projectiles[:]:
                    if proj.colliderect(pygame.Rect(player_x - PLAYER_SIZE, player_y - PLAYER_SIZE, PLAYER_SIZE * 2, PLAYER_SIZE * 2)):
                        enemy.projectiles.remove(proj)
                        LIVES -= 1
                        if LIVES <= 0:
                            return "hit", enemy_vel_base, max_add_increment, score
                        return "restart", max_enemy_vel, max_add_increment, score

            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            elif triangle_collision(player_points, enemy.get_rect()):
                enemies.remove(enemy)
                LIVES -= 1
                if LIVES <= 0:
                    return "hit", enemy_vel_base, max_add_increment, score
                return "restart", max_enemy_vel, max_add_increment, score

            for proj in projectiles[:]:
                if enemy.get_rect().colliderect(proj):
                    if isinstance(enemy, BumblebeeShip):
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            score += 2
                    elif isinstance(enemy, WaspShip):
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            score += 3
                    else:
                        enemies.remove(enemy)
                        score += 1

                    projectiles.remove(proj)
                    break

        if elapsed_time > 10:
            return "level_up", enemy_vel_base, max_add_increment, score

        draw(player_x, player_y, elapsed_time, enemies, projectiles, LIVES, level, score)




def main():
    global LIVES
    run = True
    level = 1
    score = 0
    max_enemy_vel = BASE_ENEMY_VEL
    max_add_increment = BASE_ENEMY_ADD_INCREMENT

    while run:
        result, max_enemy_vel, max_add_increment, score = game_loop(level, max_enemy_vel, max_add_increment, score)
        if result == "quit":
            run = False
        elif result == "hit":
            if LIVES == 0:
                lost_text = FONT.render(f"LMAOOOOOOO u are horrible at this game. Final Score: {score}", 1, "white")  
                WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2))
                pygame.display.update()
                pygame.time.delay(4000)
                run = False
        elif result == "restart":
            continue  
        elif result == "level_up":
            level_complete_message(level)
            level += 1
            max_enemy_vel += ENEMY_VEL_INCREMENT
            max_add_increment = max(400, max_add_increment - ENEMY_ADD_DECREMENT)

    pygame.quit()

if __name__ == "__main__":
    main()