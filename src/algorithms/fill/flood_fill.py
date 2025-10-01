import pygame
from collections import deque

class FloodFill:
    def __init__(self):
        self.name = "Flood Fill"
    
    def scanline_fill(self, canvas, start_x, start_y, fill_color, boundary_color=None):
        width, height = canvas.width, canvas.height
        
        if boundary_color is None:
            boundary_color = (255, 255, 255)
        
        pixels = pygame.surfarray.pixels2d(canvas.surface)
        
        fill_color_int = self._color_to_int(fill_color)
        boundary_color_int = self._color_to_int(boundary_color)
        background_color_int = pixels[start_x, start_y]
        
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
            
            left_x = x
            while left_x > 0 and pixels[left_x - 1, y] == background_color_int:
                left_x -= 1
            
            right_x = x
            while right_x < width - 1 and pixels[right_x + 1, y] == background_color_int:
                right_x += 1
            
            for fill_x in range(left_x, right_x + 1):
                pixels[fill_x, y] = fill_color_int
            
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
        
        del pixels
    
    def _color_to_int(self, color):
        if isinstance(color, tuple) and len(color) >= 3:
            return (color[0] << 16) | (color[1] << 8) | color[2]
        return color