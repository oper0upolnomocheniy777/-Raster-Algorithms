import pygame
from collections import deque

class FloodFill:
    def __init__(self):
        self.name = "Flood Fill"
    
    def scanline_fill(self, canvas, start_x, start_y, fill_color, boundary_color=None):
        """Рекурсивная заливка на основе серий пикселов"""
        width, height = canvas.width, canvas.height
        
        # Если boundary_color не указан, используем текущий цвет границы
        if boundary_color is None:
            boundary_color = (255, 255, 255)  # белый по умолчанию
        
        # Получаем пиксели холста
        pixels = pygame.surfarray.pixels2d(canvas.surface)
        
        # Конвертируем цвета в integer representation
        fill_color_int = self._color_to_int(fill_color)
        boundary_color_int = self._color_to_int(boundary_color)
        background_color_int = pixels[start_x, start_y]
        
        # Проверяем, не пытаемся ли залить границу или уже залитую область
        if (background_color_int == fill_color_int or 
            background_color_int == boundary_color_int):
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
            while left_x > 0 and pixels[left_x - 1, y] == background_color_int:
                left_x -= 1
            
            # Находим правую границу  
            right_x = x
            while right_x < width - 1 and pixels[right_x + 1, y] == background_color_int:
                right_x += 1
            
            # Заливаем сегмент
            for fill_x in range(left_x, right_x + 1):
                pixels[fill_x, y] = fill_color_int
            
            # Проверяем строки выше и ниже
            for scan_y in [y - 1, y + 1]:
                if 0 <= scan_y < height:
                    span_added = False
                    for scan_x in range(left_x, right_x + 1):
                        if (scan_x < width and 
                            pixels[scan_x, scan_y] == background_color_int and 
                            (scan_x, scan_y) not in visited):
                            
                            if not span_added:
                                stack.append((scan_x, scan_y))
                                span_added = True
                        else:
                            span_added = False
        
        # Освобождаем массив пикселей
        del pixels
    
    def _color_to_int(self, color):
        """Конвертирует RGB цвет в integer representation"""
        if isinstance(color, tuple) and len(color) >= 3:
            return (color[0] << 16) | (color[1] << 8) | color[2]
        return color