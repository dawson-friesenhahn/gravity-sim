import pygame
from dotenv import load_dotenv
import os
from pygame.math import Vector2
import numpy as np
from typing import List, Self
import logging
logger = logging.getLogger(__name__)

load_dotenv()
BIG_G = float(os.getenv('BIG_G'))
FPS = float(os.getenv('FPS'))

class MassiveBodyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def add(self, *sprites):
        for sprite in sprites:
            if not isinstance(sprite, MassiveBody):
                raise ValueError("Only MassiveBodies can be contained in MassiveBodyGroups!")
        pygame.sprite.Group.add(self, *sprites) 

    def update(self, *args, **kwargs):
        for body in self:
            body.update_velocity(self.sprites())
        super().update(*args, **kwargs)


class MassiveBody(pygame.sprite.Sprite):
    _body_id = 0
    def __init__(self, mass: float, image: pygame.surface.Surface, x: int, y: int):
        super().__init__()
        self.image = image 
        self.rect = self.image.get_rect(center = (x,y) )
        self.mass = mass
        self.velocity = np.array([0, 0], dtype=np.float32)
        self.id = MassiveBody._body_id
        self.collission_this_frame = False
        MassiveBody._body_id +=1

    def get_center(self) ->np.array:
        return np.array(self.rect.center)
    
    def update_velocity(self, massiveBodies, additional_force = None):
        if additional_force is None:
            additional_force = np.array([0,0], dtype=np.float32)
        force_vector = additional_force
        logger.debug(self)
        logger.debug(f"\tOld Velocity: {self.velocity}")
        for body in massiveBodies:
            if body == self:
                continue
            if pygame.sprite.collide_circle(self, body):
                logger.debug(f"\tCOLLISION!")
                if not self.collission_this_frame:
                    speed = np.linalg.norm(self.velocity)
                    new_velocity = self.calculate_velocity_after_collission(body)
                    body.velocity = body.calculate_velocity_after_collission(self)
                    body.collission_this_frame = True
                    self.collission_this_frame = True
                    self.velocity = new_velocity
                    #new_position = self.calculate_new_position_after_collission(body)
                    #self.rect.x = new_position[0]
                    #self.rect.y = new_position[1]
                    logger.debug(f"\tNew velocity: {self.velocity}")
                continue
            force_vector += calculate_force_vector(self, body)
        self.collission_this_frame = False
        logger.debug(f"\tForce: {force_vector}")
        delta_v = calculate_delta_v(self, force_vector)
        logger.debug(f"\tDelta V: {delta_v}")
        self.velocity += delta_v
        logger.debug(f"\tNew Velocity: {self.velocity}\n")

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
    def calculate_velocity_after_collission(self, other: Self):
        '''Stolen from https://en.wikipedia.org/wiki/Elastic_collision'''
        return self.velocity - (2*other.mass)/(self.mass + other.mass) * ((self.velocity - other.velocity).dot(self.get_center() - other.get_center()))/(np.linalg.norm(self.get_center() - other.get_center()) **2) * (self.get_center() - other.get_center()) 
    
    def calculate_new_position_after_collission(self, other:Self):
        '''this don't work right, looks weird'''
        direction_to_move = (self.get_center() - other.get_center()) / np.linalg.norm(self.get_center() - other.get_center())
        #print(f"Direction: {direction_to_move}")
        try:
            minimum_separation = self.radius + other.radius
        except:
            minimum_separation = max(self.rect.width, self.rect.height)/2 + max(other.rect.width, other.rect.height)/2
        
        #print(f"Min sep: {minimum_separation}")
        new_position = other.get_center() + direction_to_move * minimum_separation
        return new_position


    def __repr__(self):
        return f"MassiveBody {self.id} at {self.get_center()}"
    
    def __eq__(self, other):
        if isinstance(other, MassiveBody):
            return self.id == other.id
        else:
            return False
    
    def __hash__(self):
        return hash((self.id) )


def calculate_force_vector(body1: MassiveBody, body2: MassiveBody) ->np.array:
    '''returns force vector from body1 to body2. Negating returns vector from body2 to body1'''
    r_sq = np.linalg.norm(body1.get_center() - body2.get_center()) **2
    if np.isclose(r_sq, 0):
        return 0
    force_magnitude =  (BIG_G * body1.mass * body2.mass) / r_sq
    return np.array((body2.get_center() - body1.get_center()) * force_magnitude, np.float32)

def calculate_delta_v(body1: MassiveBody, force: np.array):
    return force/body1.mass * (1/FPS)


if __name__ == "__main__":
    body1_coord = (305,301)
    image1 = pygame.Surface((20, 20))
    pygame.draw.circle(surface=image1, color=(0,0,255), center=(10,10), radius=10)
    body1 = MassiveBody(mass=10, image=image1, x=body1_coord[0], y=body1_coord[1])
    body1.velocity[0] = 0.5

    body2_coord = (310, 300)
    image2 = pygame.Surface((20, 20))
    pygame.draw.circle(image2, (255,0,0), center=(10,10), radius=10)
    body2 = MassiveBody(10, image2, body2_coord[0], body2_coord[1])
    body2.velocity[0] = 0.5

    print(body1.calculate_new_position_after_collission(body2))
