import pygame
from MassiveBody import MassiveBody, MassiveBodyGroup
from Player import Player
from dotenv import load_dotenv
import os
import logging
from util import draw_arrow
from pygame import Vector2



logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'grav.log', filemode='w', level=logging.INFO)

load_dotenv()
SCREEN_WIDTH = int(os.getenv('SCREEN_WIDTH'))
SCREEN_HEIGHT = int(os.getenv('SCREEN_HEIGHT'))
FPS = int(os.getenv('FPS'))

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity, Boiiiii")

clock= pygame.time.Clock()

body1_coord = (400,400)
image1 = pygame.Surface((30, 30))
pygame.draw.circle(surface=image1, color=(0,0,255), center=(15,15), radius=15)
body1 = MassiveBody(mass=100000, image=image1, x=body1_coord[0], y=body1_coord[1], immovable=True)
body1.velocity[0] = 0


body2_coord = (700, 400)
image2 = pygame.Surface((20, 20))
pygame.draw.circle(image2, (255,0,0), center=(10,10), radius=10)
body2 = MassiveBody(10000, image2, body2_coord[0], body2_coord[1])
body2.velocity[1] = 4

# body3_coord = (500, 350)
# image3 = pygame.Surface((20, 20))
# pygame.draw.circle(image3, (0,255,0), center=(10,10), radius=10)
# body3 = MassiveBody(1, image3, body3_coord[0], body3_coord[1])
# body3.velocity[0] = -1




player_img = pygame.image.load("smiley.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (30, 30))
player = Player(10, player_img, 300, 300)



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