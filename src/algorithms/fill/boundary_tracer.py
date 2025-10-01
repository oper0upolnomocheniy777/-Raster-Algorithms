import pygame

class BoundaryTracer:
    def __init__(self):
        self.name = "Boundary Tracer"
        self.directions = [
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1)
        ]
    
    def trace_boundary(self, canvas, start_x, start_y, boundary_color):
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
        
        current_x, current_y = start_x, start_y
        direction = 0
        
        while True:
            boundary_points.append((current_x, current_y))
            visited.add((current_x, current_y))
            
            found_next = False
            for i in range(8):
                check_dir = (direction + 5 + i) % 8
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
        
        if boundary_points and boundary_points[0] != boundary_points[-1]:
            boundary_points.append(boundary_points[0])
        
        del pixels
        return boundary_points
    
    def draw_boundary(self, surface, boundary_points, color=(0, 255, 0)):
        if len(boundary_points) > 1:
            pygame.draw.lines(surface, color, False, boundary_points, 2)
    
    def _color_to_int(self, color):
        if isinstance(color, tuple) and len(color) >= 3:
            return (color[0] << 16) | (color[1] << 8) | color[2]
        return color