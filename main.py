import os
import pygame
import pygame.locals
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# world configs
background = pygame.transform.scale(pygame.image.load(os.path.join('assets/background', 'background.png')), (1280, 720))
grass = pygame.transform.scale(pygame.image.load(os.path.join('assets/background', 'grass.png')), (1280, 720))
backgorund_position = 0
ground_height = 720 // 2 - 50
gravity = 0.9

# obstacles config
is_spawned = False
obstacle_hitbox = []

# rock configs
rock_sprites = [pygame.image.load(os.path.join('assets/obstacles/rocks', 'rock.png')), pygame.image.load(os.path.join('assets/obstacles/rocks', 'big_rock.png'))]

# bird configs
bird_sprites = [pygame.image.load(os.path.join('assets/obstacles/bird', 'bird_1.png')), pygame.image.load(os.path.join('assets/obstacles/bird', 'bird_2.png'))]

x_obstacle = 1280 - 60
obstacle_velocity = -10

# player configs
player = [pygame.image.load(os.path.join('assets/ovo_images', 'egg.png')), pygame.image.load(os.path.join('assets/ovo_images', 'jump_egg.png')), pygame.transform.scale(pygame.image.load(os.path.join('assets/ovo_images', 'game_over.png')), (84, 74))]
x_player, y_player = 90, ground_height
y_velocity = 0
jump_force = -13
in_air = False
player_hitbox = pygame.Rect(x_player, y_player, player[1].get_width(), player[1].get_height())

# Initial variables for animation
frame_index = 0
last_update = pygame.time.get_ticks()
animation_speed = 110

# walk sound
walk = pygame.mixer.Sound(os.path.join('assets/sounds', 'walk.mp3')).play(loops=-1)

# Set up the font and text
font = pygame.font.SysFont('Monospace', 36)
text = font.render('Press any key to continue', True, (0, 0, 0))

# Function to display the start screen
def show_start_screen():
    screen.fill((255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
    pygame.display.flip()

# Function to reset the game
def reset_game():
    global x_player, y_player, y_velocity, in_air, is_spawned, x_obstacle, obstacle_hitbox, backgorund_position
    x_player, y_player = 90, ground_height
    y_velocity = 0
    in_air = False
    is_spawned = False
    x_obstacle = 1280 - 60
    backgorund_position = 0

while running:
    show_start_screen()  # Show start screen initially
    waiting_for_input = True

    # Wait for any key press to start or restart the game
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            elif event.type == pygame.KEYDOWN:
                waiting_for_input = False
                reset_game()  # Reset game variables to start a new game

    # Game logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Control animations
        now = pygame.time.get_ticks()
        if now - last_update > animation_speed:
            last_update = now
            frame_index += 1
            
            if frame_index >= len(bird_sprites):
                frame_index = 0

        # Setup background and screen updates
        screen.fill("black")
        screen.blit(background, (backgorund_position, 0))

        if backgorund_position <= -10:
            new_background = backgorund_position + 1280
            screen.blit(background, (new_background, 0))
            screen.blit(grass, (new_background, 0))

        # Rock and bird spawn logic
        if not is_spawned:
            not_is_bird = random.randint(0, 1)

            if not_is_bird:
                obstacle = rock_sprites[random.randint(0, 1)]
                y_obstacle = ground_height
                obstacle_hitbox = pygame.Rect(x_obstacle, y_obstacle, obstacle.get_width(), obstacle.get_height())
            else:
                obstacle = bird_sprites
                y_obstacle = random.choice([ground_height, ground_height - 62, ground_height - 16])
                obstacle_hitbox = pygame.Rect(x_obstacle, y_obstacle, obstacle[0].get_width(), obstacle[0].get_height())

            is_spawned = not is_spawned

        else:
            if not_is_bird:
                x_obstacle += obstacle_velocity
                obstacle_hitbox.x = x_obstacle
                screen.blit(obstacle, (x_obstacle, y_obstacle))
            else:
                x_obstacle += obstacle_velocity - 5
                obstacle_hitbox.x = x_obstacle
                screen.blit(obstacle[frame_index], (x_obstacle, y_obstacle))

            if x_obstacle <= -5:
                is_spawned = not is_spawned
                x_obstacle = 1280 - 80

        # Interface (player movement)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not in_air:
            pygame.mixer.Sound(os.path.join('assets/sounds', 'jump.mp3')).play()
            y_velocity = jump_force
            in_air = True

        if in_air:
            screen.blit(player[1], (x_player, y_player))
            y_velocity += gravity

        if not in_air:
            screen.blit(player[0], (x_player, y_player))

        y_player += y_velocity
        if y_player > ground_height:  # Hit the ground
            y_player = ground_height
            in_air = False
            y_velocity = 0

        player_hitbox.y = y_player

        # Collision detection
        if player_hitbox.colliderect(obstacle_hitbox):
            screen.blit(background, (backgorund_position, 0))
            screen.blit(obstacle if not_is_bird else obstacle[frame_index], (x_obstacle, y_obstacle))
            screen.blit(grass, (backgorund_position, 1))
            screen.blit(player[2], (x_player, y_player))
            pygame.mixer.Sound(os.path.join('assets/sounds', 'egg-cracking.mp3')).play()
            walk.stop()
            pygame.display.flip()
            pygame.time.wait(1000)

            break

        # Background scrolling
        screen.blit(grass, (backgorund_position, 1))
        backgorund_position += obstacle_velocity

        if backgorund_position == -1280:
            temp = backgorund_position
            backgorund_position = new_background
            new_background = temp

        pygame.display.flip()
        clock.tick(60)
