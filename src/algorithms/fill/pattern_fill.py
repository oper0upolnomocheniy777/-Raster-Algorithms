import pygame
import os
from collections import deque

class PatternFill:
    def __init__(self):
        self.name = "Pattern Fill"
        self.pattern = None
    
    def load_pattern(self, filename):
        """Загружает паттерн из файла"""
        try:
            if os.path.exists(filename):
                pattern_surface = pygame.image.load(filename)
                self.pattern = pattern_surface.convert()
                return True
            
            # Проверяем в папке patterns
            pattern_path = os.path.join("patterns", filename)
            if os.path.exists(pattern_path):
                pattern_surface = pygame.image.load(pattern_path)
                self.pattern = pattern_surface.convert()
                return True
            
            print(f"Pattern file {filename} not found")
            return False
            
        except pygame.error as e:
            print(f"Error loading pattern: {e}")
            return False
    
    def pattern_fill(self, canvas, start_x, start_y, boundary_color=None):
        """Заливка рисунком из графического файла"""
        if self.pattern is None:
            print("No pattern loaded")
            return
        
        width, height = canvas.width, canvas.height
        pattern_width, pattern_height = self.pattern.get_size()
        
        # Получаем пиксели холста и паттерна
        canvas_pixels = pygame.surfarray.pixels2d(canvas.surface)
        pattern_pixels = pygame.surfarray.pixels2d(self.pattern)
        
        if boundary_color is None:
            boundary_color = (255, 255, 255)
        
        boundary_color_int = self._color_to_int(boundary_color)
        background_color_int = canvas_pixels[start_x, start_y]
        
        if background_color_int == boundary_color_int:
            return
        
        stack = deque()
        stack.append((start_x, start_y))
        visited = set()
        
        while stack:
            x, y = stack.pop()
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            # Находим левую границу
            left_x = x
            while left_x > 0 and canvas_pixels[left_x - 1, y] == background_color_int:
                left_x -= 1
            
            # Находим правую границу
            right_x = x
            while right_x < width - 1 and canvas_pixels[right_x + 1, y] == background_color_int:
                right_x += 1
            
            # Заливаем сегмент паттерном
            for fill_x in range(left_x, right_x + 1):
                if canvas_pixels[fill_x, y] == background_color_int:
                    pattern_x = fill_x % pattern_width
                    pattern_y = y % pattern_height
                    canvas_pixels[fill_x, y] = pattern_pixels[pattern_x, pattern_y]
            
            # Проверяем строки выше и ниже
            for scan_y in [y - 1, y + 1]:
                if 0 <= scan_y < height:
                    span_added = False
                    for scan_x in range(left_x, right_x + 1):
                        if (scan_x < width and 
                            canvas_pixels[scan_x, scan_y] == background_color_int and 
                            (scan_x, scan_y) not in visited):
                            
                            if not span_added:
                                stack.append((scan_x, scan_y))
                                span_added = True
                        else:
                            span_added = False
        
        # Освобождаем массивы пикселей
        del canvas_pixels
        del pattern_pixels
    
    def _color_to_int(self, color):
        """Конвертирует RGB цвет в integer representation"""
        if isinstance(color, tuple) and len(color) >= 3:
            return (color[0] << 16) | (color[1] << 8) | color[2]
        return color