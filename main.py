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
rock_tipes = [pygame.image.load(os.path.join('assets/obstacles/rocks', 'rock.png')), pygame.image.load(os.path.join('assets/obstacles/rocks', 'big_rock.png'))]
x_rock = 1280 - 60
rock_velocity = 10
is_spawned = False
rock_rects = []

# player configs
player = [pygame.image.load(os.path.join('assets/ovo_images', 'egg.png')), pygame.image.load(os.path.join('assets/ovo_images', 'jump_egg.png'))]
x_player, y_player = 80, ground_height
y_velocity = 0
jump_force = -13
in_air = False
player_rects = pygame.Rect(x_player, y_player, player[0].get_width(), player[0].get_height())

# walk sound
pygame.mixer.Sound(os.path.join('assets/sounds', 'walk.mp3')).play(loops=-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # update hitbox position
    player_rects.topleft = (x_player, y_player)

    # rock spawn and logic
    if not is_spawned:
        rock = rock_tipes[random.randint(0, 1)]
        rock_rect = pygame.Rect(x_rock, ground_height, rock.get_width(), rock.get_height())
        rock_rects.append(rock_rect)
        is_spawned = True

    elif is_spawned:
        for rock, rock_rect in zip(rock_tipes, rock_rects):
            screen.blit(rock, rock_rect.topleft)
            rock_rect.x -= rock_velocity

        rock_rects = [r for r in rock_rects if r.x > 0]

        if len(rock_rects) == 1:
            x_rock = 1280 - 60
            is_spawned = False

    # colision
    for rock_rect in rock_rects:
        if player_rects.colliderect(rock_rect):
            print('fim da linha')
            running = False

    #setup 2
    screen.blit(grass, (backgorund_position, 1))
    backgorund_position -= rock_velocity

    if backgorund_position == -1280:
        temp = backgorund_position
        backgorund_position = new_background
        new_background = temp

    pygame.display.flip()
    clock.tick(60)
