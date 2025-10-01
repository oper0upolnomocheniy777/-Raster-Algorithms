import pygame
import sys
from core.canvas import Canvas
from algorithms.lines.bresenham import bresenham_line
from algorithms.lines.wu import wu_line
from algorithms.triangle.gradient_triangle import draw_gradient_triangle, draw_triangle_outline

# НОВЫЕ ИМПОРТЫ ДЛЯ ЗАЛИВКИ
from algorithms.fill import FloodFill, PatternFill, BoundaryTracer

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Computer Graphics - Fill Algorithms")

# Создаем холст
canvas = Canvas(WIDTH, HEIGHT)

# Переменные для рисования
drawing = False
start_pos = None
current_algorithm = "bresenham"
line_color = (255, 255, 255)

# Переменные для треугольника
current_mode = "line"
triangle_vertices = []

# НОВЫЕ ПЕРЕМЕННЫЕ ДЛЯ РЕЖИМА ЗАЛИВКИ
fill_algorithms = {
    "flood": FloodFill(),
    "pattern": PatternFill(),
    "boundary": BoundaryTracer()
}
current_fill_algorithm = "flood"
fill_color = (255, 0, 0)  # красный по умолчанию
boundary_color = (255, 255, 255)  # белый для границ

def draw_interface():
    """Рисует интерфейс"""
    font = pygame.font.SysFont(None, 24)
    
    mode_text = f"Mode: {current_mode.upper()}"
    text_surface = font.render(mode_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    if current_mode == "line":
        algo_text = f"Line Algorithm: {current_algorithm.upper()}"
    elif current_mode == "triangle":
        algo_text = "Triangle: Click 3 points for gradient triangle"
    else:  # fill mode
        algo_text = f"Fill: {fill_algorithms[current_fill_algorithm].name}"
    
    algo_surface = font.render(algo_text, True, (255, 255, 255))
    screen.blit(algo_surface, (10, 40))
    
    # ОБНОВЛЕННАЯ ИНСТРУКЦИЯ
    instr_lines = [
        "L: Line mode | T: Triangle mode | F: Fill mode",
        "SPACE: Switch algorithms | C: Clear canvas",
        "1-3: Colors | 4: Random color | P: Load pattern",
        "B: Boundary trace | R: Reset fill mode"
    ]
    
    for i, line in enumerate(instr_lines):
        instr_surface = font.render(line, True, (200, 200, 200))
        screen.blit(instr_surface, (10, HEIGHT - 100 + i * 25))

def get_random_color():
    """Возвращает случайный цвет"""
    import random
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    global drawing, start_pos, current_algorithm, line_color
    global current_mode, triangle_vertices
    global current_fill_algorithm, fill_color, boundary_color
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    pos = event.pos
                    
                    if current_mode == "line":
                        drawing = True
                        start_pos = pos
                    
                    elif current_mode == "triangle":
                        triangle_vertices.append(pos)
                        if len(triangle_vertices) == 3:
                            x1, y1 = triangle_vertices[0]
                            x2, y2 = triangle_vertices[1]
                            x3, y3 = triangle_vertices[2]
                            
                            color1 = line_color
                            color2 = get_random_color()
                            color3 = get_random_color()
                            
                            draw_gradient_triangle(canvas, x1, y1, color1, x2, y2, color2, x3, y3, color3)
                            draw_triangle_outline(canvas, x1, y1, x2, y2, x3, y3, (255, 255, 255))
                            triangle_vertices = []
                    
                    # НОВЫЙ РЕЖИМ: ЗАЛИВКА
                    elif current_mode == "fill":
                        x, y = pos
                        
                        if current_fill_algorithm == "flood":
                            fill_algorithms["flood"].scanline_fill(
                                canvas, x, y, fill_color, boundary_color
                            )
                        
                        elif current_fill_algorithm == "pattern":
                            fill_algorithms["pattern"].pattern_fill(
                                canvas, x, y, boundary_color
                            )
                        
                        elif current_fill_algorithm == "boundary":
                            boundary_points = fill_algorithms["boundary"].trace_boundary(
                                canvas, x, y, boundary_color
                            )
                            # Временно рисуем границу поверх
                            temp_surface = screen.copy()
                            fill_algorithms["boundary"].draw_boundary(
                                temp_surface, boundary_points, (0, 255, 0)
                            )
                            screen.blit(temp_surface, (0, 0))
                            pygame.display.flip()
                            pygame.time.delay(2000)  # Показываем 2 секунды
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing and current_mode == "line":
                    drawing = False
                    end_pos = event.pos
                    
                    if current_algorithm == "bresenham":
                        bresenham_line(canvas, start_pos[0], start_pos[1], 
                                     end_pos[0], end_pos[1], line_color)
                    else:
                        wu_line(canvas, start_pos[0], start_pos[1], 
                              end_pos[0], end_pos[1], line_color)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_mode == "line":
                        current_algorithm = "wu" if current_algorithm == "bresenham" else "bresenham"
                    elif current_mode == "fill":
                        # Переключаем алгоритмы заливки
                        algorithms = list(fill_algorithms.keys())
                        current_index = algorithms.index(current_fill_algorithm)
                        current_fill_algorithm = algorithms[(current_index + 1) % len(algorithms)]
                
                # Переключение режимов
                elif event.key == pygame.K_l:
                    current_mode = "line"
                    triangle_vertices = []
                
                elif event.key == pygame.K_t:
                    current_mode = "triangle"
                    triangle_vertices = []
                
                elif event.key == pygame.K_f:  # НОВЫЙ РЕЖИМ
                    current_mode = "fill"
                    triangle_vertices = []
                
                elif event.key == pygame.K_c:
                    canvas.clear()
                    triangle_vertices = []
                
                # Управление цветами
                elif event.key == pygame.K_1:
                    line_color = (255, 0, 0)
                    fill_color = (255, 0, 0)
                
                elif event.key == pygame.K_2:
                    line_color = (0, 255, 0)
                    fill_color = (0, 255, 0)
                
                elif event.key == pygame.K_3:
                    line_color = (0, 0, 255)
                    fill_color = (0, 0, 255)
                
                elif event.key == pygame.K_4:
                    random_color = get_random_color()
                    if current_mode == "triangle":
                        line_color = random_color
                    elif current_mode == "fill":
                        fill_color = random_color
                
                # НОВЫЕ КЛАВИШИ ДЛЯ ЗАЛИВКИ
                elif event.key == pygame.K_p and current_mode == "fill":
                    # Загрузка паттерна
                    if fill_algorithms["pattern"].load_pattern("pattern.png"):
                        print("Pattern loaded successfully")
                    else:
                        print("Failed to load pattern")
                
                elif event.key == pygame.K_r:
                    # Сброс режима заливки
                    if current_mode == "fill":
                        current_fill_algorithm = "flood"
        
        # Отрисовка
        screen.fill((0, 0, 0))
        canvas.draw_to_screen(screen)
        
        # Показываем текущие вершины треугольника
        if current_mode == "triangle" and triangle_vertices:
            for i, (x, y) in enumerate(triangle_vertices):
                pygame.draw.circle(screen, (255, 255, 0), (x, y), 5)
                font = pygame.font.SysFont(None, 20)
                text = font.render(f"{i+1}", True, (255, 255, 0))
                screen.blit(text, (x + 8, y - 8))
        
        draw_interface()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()