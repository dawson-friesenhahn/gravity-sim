import pygame
from MassiveBody import MassiveBody, MassiveBodyGroup
from Player import Player
import os
import logging
from pygame import Vector2



logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'grav.log', filemode='w', level=logging.DEBUG)

from Constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity, Boiiiii")

clock= pygame.time.Clock()

body1_coord = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
image1 = pygame.Surface((30, 30))
pygame.draw.circle(surface=image1, color=(0,0,255), center=(15,15), radius=15)
body1 = MassiveBody(mass=100000, image=image1, x=body1_coord[0], y=body1_coord[1], immovable=True)
body1.velocity[0] = 0


body2_coord = (SCREEN_WIDTH//2 + SCREEN_WIDTH//3, SCREEN_HEIGHT//2)
image2 = pygame.Surface((20, 20))
pygame.draw.circle(image2, (255,0,0), center=(10,10), radius=10)
body2 = MassiveBody(10000, image2, body2_coord[0], body2_coord[1])
body2.velocity[1] = 1


player_img = pygame.image.load("rocket.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (30, 30))
player = Player(10, player_img, SCREEN_WIDTH//2 - SCREEN_WIDTH//3, SCREEN_HEIGHT//2)
player.velocity[1] = -1



massive_bodies= MassiveBodyGroup()
massive_bodies.add(body1)
massive_bodies.add(body2)
#massive_bodies.add(body3)
massive_bodies.add(player)


running= True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rotate(-5)
    if keys[pygame.K_RIGHT]:
        player.rotate(5)
    if keys[pygame.K_SPACE]:
        player.spacebar_pressed()
    if keys[pygame.K_r]:
        player.reset()
    if keys[pygame.K_f]:
        for sprite in massive_bodies:
            sprite.show_force_vectors = not sprite.show_force_vectors
    if keys[pygame.K_v]:
        for sprite in massive_bodies:
            sprite.show_velocity_vector = not sprite.show_velocity_vector

    
    
    massive_bodies.update()
    logging.debug("----CLOCK TICK-----\n")

    screen.fill((0,0,0))
    massive_bodies.draw(screen)
    #draw_arrow(screen, Vector2(*player.get_center()), Vector2(*(player.get_center()) + Vector2(10,10)), (255,255,255))
    pygame.display.flip()
    clock.tick(FPS)