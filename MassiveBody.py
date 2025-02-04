import pygame
from pygame.math import Vector2
import numpy as np
from typing import List, Self
import logging
logger = logging.getLogger(__name__)
from util import draw_arrow


from Constants import BIG_G, FPS


class MassiveBodyGroup(pygame.sprite.Group):
    
    def __init__(self):
        logger.debug(f"BIG G: {BIG_G}")
        super().__init__()

    def add(self, *sprites):
        for sprite in sprites:
            if not isinstance(sprite, MassiveBody):
                raise ValueError("Only MassiveBodies can be contained in MassiveBodyGroups!")
        pygame.sprite.Group.add(self, *sprites) 

    def draw(self, screen, bgsurf=None, special_flags=0):
        super().draw(screen, bgsurf, special_flags)
        for sprite in self.sprites():
            sprite.draw(screen)

    def toggle_show_force_vectors(self):
        for sprite in self.sprites():
                sprite.show_force_vectors = not sprite.show_force_vectors
    
    def toggle_show_velocity_vectors(self):
        for sprite in self.sprites():
            sprite.show_velocity_vector = not sprite.show_velocity_vector

    def update(self, *args, **kwargs):
        for body in self:
            body.update_velocity(self.sprites())
        super().update(*args, **kwargs)


class MassiveBody(pygame.sprite.Sprite):
    _body_id = 0
    def __init__(self, mass: float, image: pygame.surface.Surface, x: int, y: int, immovable = False):
        super().__init__()
        self.position = np.array([x, y], np.float32)
        self.image = image 
        self.rect = self.image.get_rect(center = (x,y) )
        self.mass = mass
        self.velocity = np.array([0, 0], dtype=np.float32)
        self.id = MassiveBody._body_id
        self.collission_this_frame = False
        self.show_force_vectors = False
        self.show_velocity_vector = False
        self.arrow_params = []
        self.immovable = immovable
        MassiveBody._body_id +=1

    def get_center(self) ->np.array:
        return self.position
    
    def add_force_vector_arrow(self, target, magnitude):
        start = Vector2(*(self.get_center()+ self.velocity))
        direction = (target - start) / np.linalg.norm(target - start)
        end = start + (direction * magnitude /self.mass * 10)
        params = (start, end, (255, 255, 255))
        logger.debug(f"Force vector direction: {direction}")
        logger.debug(f"force vector: <{start} , {end}>")
        self.arrow_params.append(params)
    
    def add_velocity_vector(self):
        start = Vector2(*(self.get_center()+ self.velocity))
        end = start + Vector2(*(self.velocity* 10))
        params = (start, end, (0, 255, 0))
        self.arrow_params.append(params)

    def draw(self, screen):
        for params in self.arrow_params:
            draw_arrow(screen, *params)

    def update_velocity(self, massiveBodies, additional_force = None):
        if self.immovable:
            return
        self.arrow_params.clear()
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
            force_vector_this_body =  calculate_force_vector(self, body)
            if self.show_force_vectors:
                self.add_force_vector_arrow(body.get_center(), np.linalg.norm(force_vector_this_body))
            force_vector += force_vector_this_body
        self.collission_this_frame = False
        logger.debug(f"\tForce: {force_vector}")
        delta_v = calculate_delta_v(self, force_vector)
        logger.debug(f"\tDelta V: {delta_v}")
        self.velocity += delta_v
        logger.debug(f"\tNew Velocity: {self.velocity}\n")
        if self.show_velocity_vector:
            self.add_velocity_vector()

    def update(self):
        self.position +=  self.velocity 
        self.rect.x = int(self.position[0] - self.image.get_width()//2)
        self.rect.y = int(self.position[1] - self.image.get_height()//2)
        
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
