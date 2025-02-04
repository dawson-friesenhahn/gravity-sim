import pygame


class ToggleHelper:
    def __init__(self):
        self.keys_pressed_this_frame = []
        self.keys_pressed_last_frame = []

    def key_pressed(self, key: int)-> bool:
        '''Returns true if the specified key wasn't pressed last frame, false otherwise
        
        Used to 'debounce' inputs, only take action for one keypress at a time
        
        '''
        self.keys_pressed_this_frame.append(key)
        if key in self.keys_pressed_last_frame:
            return False
        return True

    def update(self):
        self.keys_pressed_last_frame = self.keys_pressed_this_frame.copy()
        self.keys_pressed_this_frame.clear()