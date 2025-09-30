import pygame
import numpy as np

class Canvas:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.clear()
    
    def clear(self, color=(0, 0, 0)):
        """Очистить холст"""
        self.surface.fill(color)
    
    def set_pixel(self, x, y, color):
        """Установить пиксель на холсте"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.surface.set_at((x, y), color)
    
    def draw_to_screen(self, screen):
        """Нарисовать холст на экране"""
        screen.blit(self.surface, (0, 0))