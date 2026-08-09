import pygame
import random

pygame.init()

pygame.mixer.init()

crash_sound = pygame.mixer.Sound("sounds/crash.wav")
gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toyota Racing")

clock = pygame.time.Clock()

car_image = pygame.image.load("images/carr.png")
car_image = pygame.transform.rotate(car_image, -90)
car_image = pygame.transform.scale(car_image, (90, 140))
enemy_images = [

    pygame.transform.scale(
        pygame.transform.rotate(pygame.image.load("images/carr.png"), -90),
       (90, 140)
    ),
    pygame.transform.scale(
        pygame.transform.rotate(pygame.image.load("images/car2.png"), -360),
        (90, 140)
    ),
    pygame.transform.scale(
        pygame.transform.rotate(pygame.image.load("images/car3.png"), -360),
        (90, 140)
    )
]
tree_image = pygame.image.load("images/tree.png")
tree_image = pygame.transform.scale(tree_image, (80, 100))
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

running = True
game_over = False

car_x = 370
car_y = 450
line_y = 0
score = 0
crash_effect = 0
best_score = 0
lives = 3

enemies = [
    [270, -100, 5, random.choice(enemy_images)],
    [400, -300, 5, random.choice(enemy_images)],
    [530, -500, 5, random.choice(enemy_images)]
]


def move_enemy(enemy):
    enemy[1] += enemy[2]


def draw_enemy(enemy):
    screen.blit(enemy[3], (enemy[0], enemy[1]))


def reset_enemy(enemy):
    enemy[1] = -100
    lanes = [220, 350, 480]
    enemy[0] = random.choice(lanes)

    enemy[3] = random.choice(enemy_images)


def add_score(score):
    return score + 1


def check_collision(car_x, car_y, enemy):
    return abs(car_x - enemy[0]) < 60 and abs(car_y - enemy[1]) < 100


def restart_game():
    global score, car_x, car_y, game_over, started, lives

    score = 0
    lives = 3
    car_x = 370
    car_y = 450

    game_over = False
    started = True


    for enemy in enemies:
        enemy[2] = 5
        reset_enemy(enemy)

    game_over = False
started = False
paused = False
while running:

    line_y += 2
    if line_y >= 120:
        line_y = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:



            if not started and event.key == pygame.K_SPACE:
                started = True

            if game_over and event.key == pygame.K_r:
                restart_game()

            if started and not game_over and event.key == pygame.K_p:
                paused = not paused

    if not started:
        screen.fill((40, 40, 40))

        title = game_over_font.render("TOYOTA RACING", True, (255, 255, 255))
        screen.blit(title, (170, 200))

        start_text = font.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(start_text, (230, 300))

        if paused:
            pause_text = game_over_font.render(
                "PAUSED",
                True,
                (255, 255, 255)
            )
            screen.blit(pause_text, (280, 220))

            pause_hint = font.render(
                "Press P to continue",
                True,
                (255, 255, 255)
            )
            screen.blit(pause_hint, (260, 300))

        pygame.display.flip()
        clock.tick(60)
        continue



    if not game_over and not paused:




        pygame.draw.rect(screen, (30, 120, 30), (0, 0, 200, 600))
        pygame.draw.rect(screen, (30, 120, 30), (600, 0, 200, 600))

        pygame.draw.rect(screen, (80, 80, 80), (200, 0, 400, 600))
        for y in range(-100, 700, 60):
            pygame.draw.rect(screen, (255, 255, 255), (333, y + line_y, 5, 30))
            pygame.draw.rect(screen, (255, 255, 255), (466, y + line_y, 5, 30))

        pygame.draw.rect(screen, (220, 220, 220), (195, 0, 5, 600))
        pygame.draw.rect(screen, (220, 220, 220), (600, 0, 5, 600))


        for y in range(-100, 700, 120):
            screen.blit(tree_image, (40, y + line_y))
            screen.blit(tree_image, (680, y + line_y))

        for y in range(-40, 700, 80):
            pygame.draw.rect(screen, (50, 160, 50),(0, y + line_y, 200, 10))
            pygame.draw.rect(screen, (50, 160, 50), (600, y + line_y, 200, 10))

        line_y += 5

        if line_y > 40:
            line_y = 0

        #for y in range(-40, 600, 40):
            #pygame.draw.rect(screen, (255, 255, 255), (392, y + line_y, 16, 25))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            car_x -= 5

        if keys[pygame.K_RIGHT]:
            car_x += 5

        if keys[pygame.K_UP]:
            car_y -= 5

        if keys[pygame.K_DOWN]:
            car_y += 5

        if car_x < 200:
            car_x = 200
        if car_x > 540:
            car_x = 540
        if car_y < 0:
            car_y = 0
        if car_y > 500:
            car_y = 500

        screen.blit(car_image, (car_x, car_y))

        for enemy in enemies:

            if score >= 30:
                enemy[2] = 8
            elif score >= 20:
                enemy[2] = 7
            elif score >= 10:
                enemy[2] = 6
            else:
                enemy[2] = 5

            move_enemy(enemy)
            draw_enemy(enemy)

            if enemy[1] > 600:
                reset_enemy(enemy)
                score = add_score(score)
            if score % 10 == 0:
                for enemy in enemies:
                    enemy[2] += 1

            if score > best_score:
                best_score = score

            if score >= 30:
                enemy[2] = 8
            elif score >= 20:
                enemy[2] = 7
            elif score >= 10:
                enemy[2] = 6
            else:
                enemy[2] = 5

            if check_collision(car_x, car_y, enemy):
                lives -=1
                crash_sound.play()
                reset_enemy(enemy)

                if lives <= 0 :
                 game_over = True
                 crash_effect = 10
                 gameover_sound.play()
                 gameover_sound.play()

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (20, 50))

        best_score_text = font.render(f"Best score: {best_score}", True, (255, 255, 255))
        screen.blit(best_score_text, (20, 70))

    else:

        screen.fill((40, 40, 40))
        pygame.draw.rect(screen, (80, 80, 80), (200, 0, 400, 600))

        game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (180, 220))

        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(restart_text, (240, 300))

        if crash_effect > 0:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(crash_effect * 15)
            overlay.fill((255, 0, 0))
            screen.blit(overlay, (0, 0))

            crash_effect -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()