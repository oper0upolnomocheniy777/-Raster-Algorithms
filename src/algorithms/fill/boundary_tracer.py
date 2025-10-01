import pygame

class BoundaryTracer:
    def __init__(self):
        self.name = "Boundary Tracer"
        self.directions = [
            (0, -1),   # up
            (1, -1),   # up-right
            (1, 0),    # right
            (1, 1),    # down-right
            (0, 1),    # down
            (-1, 1),   # down-left
            (-1, 0),   # left
            (-1, -1)   # up-left
        ]
    
    def trace_boundary(self, canvas, start_x, start_y, boundary_color):
        """Выделение границы связной области"""
        width, height = canvas.width, canvas.height
        pixels = pygame.surfarray.pixels2d(canvas.surface)
        
        boundary_color_int = self._color_to_int(boundary_color)
        start_pixel = pixels[start_x, start_y]
        
        if start_pixel != boundary_color_int:
            print("Start point is not on boundary")
            del pixels
            return []
        
        boundary_points = []
        visited = set()
        
        # Находим начальную точку и направление
        current_x, current_y = start_x, start_y
        direction = 0  # начинаем смотреть вверх
        
        while True:
            boundary_points.append((current_x, current_y))
            visited.add((current_x, current_y))
            
            # Ищем следующую граничную точку
            found_next = False
            for i in range(8):
                check_dir = (direction + 5 + i) % 8  # начинаем смотреть на 45 градусов левее
                dx, dy = self.directions[check_dir]
                next_x, next_y = current_x + dx, current_y + dy
                
                if (0 <= next_x < width and 0 <= next_y < height and 
                    pixels[next_x, next_y] == boundary_color_int and 
                    (next_x, next_y) not in visited):
                    
                    current_x, current_y = next_x, next_y
                    direction = check_dir
                    found_next = True
                    break
            
            if not found_next or (current_x, current_y) == (start_x, start_y):
                break
        
        # Замыкаем цикл если вернулись к началу
        if boundary_points and boundary_points[0] != boundary_points[-1]:
            boundary_points.append(boundary_points[0])
        
        del pixels
        return boundary_points
    
    def draw_boundary(self, surface, boundary_points, color=(0, 255, 0)):
        """Рисует границу поверх изображения"""
        if len(boundary_points) > 1:
            pygame.draw.lines(surface, color, False, boundary_points, 2)
    
    def _color_to_int(self, color):
        """Конвертирует RGB цвет в integer representation"""
        if isinstance(color, tuple) and len(color) >= 3:
            return (color[0] << 16) | (color[1] << 8) | color[2]
        return color