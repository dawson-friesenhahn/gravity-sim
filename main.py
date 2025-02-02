import pygame
from MassiveBody import MassiveBody, MassiveBodyGroup
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'grav.log', filemode='w', level=logging.DEBUG)

load_dotenv()
SCREEN_WIDTH = int(os.getenv('SCREEN_WIDTH'))
SCREEN_HEIGHT = int(os.getenv('SCREEN_HEIGHT'))
FPS = int(os.getenv('FPS'))

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity, Boiiiii")

clock= pygame.time.Clock()

body1_coord = (300,400)
image1 = pygame.Surface((20, 20))
pygame.draw.circle(surface=image1, color=(0,0,255), center=(10,10), radius=10)
body1 = MassiveBody(mass=10, image=image1, x=body1_coord[0], y=body1_coord[1])
body1.velocity[0] = 0.5


body2_coord = (400, 400)
image2 = pygame.Surface((20, 20))
pygame.draw.circle(image2, (255,0,0), center=(10,10), radius=10)
body2 = MassiveBody(10, image2, body2_coord[0], body2_coord[1])
body2.velocity[0] = 0.5

body3_coord = (500, 350)
image3 = pygame.Surface((20, 20))
pygame.draw.circle(image3, (0,255,0), center=(10,10), radius=10)
body3 = MassiveBody(10, image3, body3_coord[0], body3_coord[1])
body3.velocity[0] = -1


massive_bodies= MassiveBodyGroup()
massive_bodies.add(body1)
massive_bodies.add(body2)
massive_bodies.add(body3)


running= True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
    
    massive_bodies.update()
    logging.debug("----CLOCK TICK-----\n")

    screen.fill((0,0,0))
    massive_bodies.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)