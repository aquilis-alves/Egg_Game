import pygame
import random
import os

import pygame.locals

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
# rock configs
rock_tipes = [pygame.image.load(os.path.join('assets/obstacles/rocks', 'rock.png')), pygame.image.load(os.path.join('assets/obstacles/rocks', 'big_rock.png'))]
is_spawned = False

# bird configs
bird_sprites = [pygame.image.load(os.path.join('assets/obstacles/bird', 'bird_1.png')), pygame.image.load(os.path.join('assets/obstacles/bird', 'bird_2.png'))]
is_open = False

x_obstacle = 1280 - 60
obstacle_velocity = -10

# player configs
player = [pygame.image.load(os.path.join('assets/ovo_images', 'egg.png')), pygame.image.load(os.path.join('assets/ovo_images', 'jump_egg.png'))]
x_player, y_player = 80, ground_height
y_velocity = 0
jump_force = -13
in_air = False

# Initial variables for animation
frame_index = 0
last_update = pygame.time.get_ticks()
animation_speed = 110

# walk sound
pygame.mixer.Sound(os.path.join('assets/sounds', 'walk.mp3')).play(loops=-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #control animations
    now = pygame.time.get_ticks()
    if now - last_update > animation_speed:
        last_update = now
        frame_index += 1
        
        if frame_index >= len(bird_sprites):
            frame_index = 0

    # setup
    screen.fill("black")
    screen.blit(background, (backgorund_position, 0))

    if backgorund_position <= -10:
        new_background = backgorund_position + 1280
        screen.blit(background, (new_background, 0))
        screen.blit(grass, (new_background, 0))

    # interface
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not in_air:
        pygame.mixer.Sound(os.path.join('assets/sounds', 'jump.mp3')).play()
        y_velocity = jump_force
        in_air = True

    # jump fisics
    if in_air:
        screen.blit(player[1], (x_player, y_player))
        y_velocity += gravity

    if not in_air:
        screen.blit(player[0], (x_player, y_player))

    y_player += y_velocity
    if y_player > ground_height: # hit the ground
        y_player = ground_height
        in_air = False
        y_velocity = 0

    # rock and bird spawn logic
    if not is_spawned:
        is_bird = random.randint(0, 1)

        if  is_bird:
            obstacle = rock_tipes[random.randint(0, 1)]
            y_obstacle = ground_height

        else:
            obstacle = bird_sprites
            y_obstacle = random.choice([ground_height - 20, ground_height - 62, ground_height - 10])

        is_spawned = not is_spawned

    else:
        if is_bird:
            x_obstacle += obstacle_velocity
            screen.blit(obstacle, (x_obstacle, y_obstacle))

        else:
            x_obstacle += obstacle_velocity - 5
            screen.blit(obstacle[frame_index], (x_obstacle, y_obstacle))

        if x_obstacle <= -5:
            is_spawned = not is_spawned
            x_obstacle = 1280 - 80

    #setup 2
    screen.blit(grass, (backgorund_position, 1))
    backgorund_position += obstacle_velocity

    if backgorund_position == -1280:
        temp = backgorund_position
        backgorund_position = new_background
        new_background = temp

    pygame.display.flip()
    clock.tick(60)
