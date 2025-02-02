import MassiveBody
import pygame
import numpy as np
import logging

logger= logging.getLogger(__name__)

class Player(MassiveBody.MassiveBody):
    def __init__(self, mass: float, image: pygame.surface.Surface, x: int, y: int):
        self.heading = 0
        self.thrusting = False
        self.thrust_magnitude = 100
        self.original_image = image
        super().__init__(mass, image, x, y)

    def rotate(self, direction_deg: float):
       self.heading = (self.heading + direction_deg) % 360
       self.image = pygame.transform.rotate(self.original_image, (360 - (self.heading)) % 360)
       original_loc = self.get_center()
       self.rect = self.image.get_rect(center=(original_loc[0], original_loc[1]))


    def spacebar_pressed(self):
        self.thrusting = True
        
    
    def reset(self):
        self.rotate(-self.heading)
        self.thrusting= False
        self.rect = self.image.get_rect(center = (300, 300))
        self.velocity = np.array([0,0], dtype=np.float32)
        

    def _heading_to_rad_properly_rotated(self):
        '''
        360 becomes 90
        90 becomes 0
        180 becomes 270
        270 becomes 180

        
        '''
        heading_deg_rotated = (self.heading + 270) % 360
        return np.deg2rad(heading_deg_rotated)

    def update_velocity(self, massiveBodies, additional_force=None):
        if additional_force is None:
            additional_force = np.array([0,0], dtype=np.float32)
        if self.thrusting:
            self.thrusting = False # reset thrusting each frame so we can detect when spacebar is released
            force_direction = np.array([np.cos(self._heading_to_rad_properly_rotated()), np.sin(self._heading_to_rad_properly_rotated())])
            additional_force = force_direction * self.thrust_magnitude
            logger.debug(f"Thrust force: {additional_force}")
        return super().update_velocity(massiveBodies, additional_force)

    def __repr__(self):
        return f"Player located at {self.get_center()}"

    def update(self):
        return super().update()