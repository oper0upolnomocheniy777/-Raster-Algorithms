import pygame
import sys
from core.canvas import Canvas
from algorithms.lines.bresenham import bresenham_line
from algorithms.lines.wu import wu_line
from algorithms.triangle.gradient_triangle import draw_gradient_triangle, draw_triangle_outline

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Computer Graphics - Line Algorithms")

# Создаем холст
canvas = Canvas(WIDTH, HEIGHT)

# Переменные для рисования - ВЫНЕСЕНО В ГЛОБАЛЬНУЮ ОБЛАСТЬ
drawing = False
start_pos = None
current_algorithm = "bresenham"  # или "wu"
line_color = (255, 255, 255)  # Белый цвет

# НОВЫЕ ПЕРЕМЕННЫЕ ДЛЯ РЕЖИМА ТРЕУГОЛЬНИКА
current_mode = "line"  # "line" или "triangle"
triangle_vertices = []  # Хранит вершины треугольника

def draw_interface():
    """Рисует интерфейс"""
    font = pygame.font.SysFont(None, 24)
    
    # ОБНОВЛЕНО: Отображаем текущий режим и алгоритм
    mode_text = f"Mode: {current_mode.upper()}"
    text_surface = font.render(mode_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    if current_mode == "line":
        algo_text = f"Line Algorithm: {current_algorithm.upper()}"
    else:
        algo_text = "Triangle: Click 3 points for gradient triangle"
    
    algo_surface = font.render(algo_text, True, (255, 255, 255))
    screen.blit(algo_surface, (10, 40))
    
    # ОБНОВЛЕНО: Инструкция
    instr_lines = [
        "L: Switch to Line mode | T: Switch to Triangle mode",
        "SPACE: Switch line algorithms | C: Clear canvas",
        "1: Red | 2: Green | 3: Blue | 4: Random colors for triangle"
    ]
    
    for i, line in enumerate(instr_lines):
        instr_surface = font.render(line, True, (200, 200, 200))
        screen.blit(instr_surface, (10, HEIGHT - 80 + i * 25))

def get_random_color():
    """Возвращает случайный цвет"""
    import random
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    # Объявляем global ПЕРЕД использованием
    global drawing, start_pos, current_algorithm, line_color
    # НОВОЕ: Добавляем новые глобальные переменные
    global current_mode, triangle_vertices
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if current_mode == "line":
                        drawing = True
                        start_pos = event.pos
                    # НОВОЕ: Режим треугольника
                    elif current_mode == "triangle":
                        # Добавляем вершину для треугольника
                        triangle_vertices.append(event.pos)
                        
                        # Если набрано 3 вершины - рисуем треугольник
                        if len(triangle_vertices) == 3:
                            x1, y1 = triangle_vertices[0]
                            x2, y2 = triangle_vertices[1]
                            x3, y3 = triangle_vertices[2]
                            
                            # Цвета вершин
                            color1 = line_color
                            color2 = get_random_color()  # Случайный цвет для второй вершины
                            color3 = get_random_color()  # Случайный цвет для третьей вершины
                            
                            # Рисуем градиентный треугольник
                            draw_gradient_triangle(canvas, x1, y1, color1, x2, y2, color2, x3, y3, color3)
                            
                            # Рисуем контур поверх заливки
                            draw_triangle_outline(canvas, x1, y1, x2, y2, x3, y3, (255, 255, 255))
                            
                            # Очищаем вершины для следующего треугольника
                            triangle_vertices = []
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing and current_mode == "line":
                    drawing = False
                    end_pos = event.pos
                    
                    # Рисуем линию выбранным алгоритмом
                    if current_algorithm == "bresenham":
                        bresenham_line(canvas, start_pos[0], start_pos[1], 
                                     end_pos[0], end_pos[1], line_color)
                    else:
                        wu_line(canvas, start_pos[0], start_pos[1], 
                              end_pos[0], end_pos[1], line_color)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # ОБНОВЛЕНО: Переключаем алгоритм только в режиме линий
                    if current_mode == "line":
                        current_algorithm = "wu" if current_algorithm == "bresenham" else "bresenham"
                
                # НОВОЕ: Переключение между режимами
                elif event.key == pygame.K_l:
                    # Переключаемся в режим линий
                    current_mode = "line"
                    triangle_vertices = []  # Очищаем вершины треугольника
                
                elif event.key == pygame.K_t:
                    # Переключаемся в режим треугольника
                    current_mode = "triangle"
                    triangle_vertices = []  # Очищаем вершины треугольника
                
                elif event.key == pygame.K_c:
                    # Очищаем холст
                    canvas.clear()
                    triangle_vertices = []  # НОВОЕ: Очищаем вершины треугольника
                
                elif event.key == pygame.K_1:
                    # Смена цвета на красный
                    line_color = (255, 0, 0)
                
                elif event.key == pygame.K_2:
                    # Смена цвета на зеленый
                    line_color = (0, 255, 0)
                
                elif event.key == pygame.K_3:
                    # Смена цвета на синий
                    line_color = (0, 0, 255)
                
                # НОВОЕ: Случайные цвета для треугольника
                elif event.key == pygame.K_4 and current_mode == "triangle":
                    # Случайные цвета для следующего треугольника
                    line_color = get_random_color()
        
        # Отрисовка
        screen.fill((0, 0, 0))  # Черный фон
        canvas.draw_to_screen(screen)
        
        # НОВОЕ: Показываем текущие вершины треугольника (если есть)
        if current_mode == "triangle" and triangle_vertices:
            for i, (x, y) in enumerate(triangle_vertices):
                pygame.draw.circle(screen, (255, 255, 0), (x, y), 5)  # Желтые точки для вершин
                font = pygame.font.SysFont(None, 20)
                text = font.render(f"{i+1}", True, (255, 255, 0))
                screen.blit(text, (x + 8, y - 8))
        
        draw_interface()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()