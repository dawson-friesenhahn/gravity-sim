import pygame
from MassiveBody import MassiveBody
from dotenv import load_dotenv
import os

load_dotenv()
SCREEN_WIDTH = int(os.getenv('SCREEN_WIDTH'))
SCREEN_HEIGHT = int(os.getenv('SCREEN_HEIGHT'))
FPS = int(os.getenv('FPS'))

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity, Boiiiii")

clock= pygame.time.Clock()

body1_coord = (200,200)
image1 = pygame.Surface((20, 20))
pygame.draw.circle(surface=image1, color=(0,0,255), center=(0,0), radius=10)
body1 = MassiveBody(mass=10, image=image1, x=body1_coord[0], y=body1_coord[1])
body1.velocity[1] = 3


body2_coord = (300, 500)
image2 = pygame.Surface((20, 20))
pygame.draw.circle(image2, (255,0,0), center=(0,0), radius=20)

body2 = MassiveBody(10, image2, body2_coord[0], body2_coord[1])
body2.velocity[1] = -3

all_sprites= pygame.sprite.Group()
all_sprites.add(body1)
all_sprites.add(body2)


running= True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
    
    MassiveBody.update_all_massivebody_velocities()
    all_sprites.update()
    print("---------\n")

    screen.fill((0,0,0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)