import pygame
import math

def draw_gradient_triangle(canvas, x1, y1, color1, x2, y2, color2, x3, y3, color3):
    """
    Рисует треугольник с градиентной заливкой используя алгоритм растеризации
    
    Args:
        canvas: холст для рисования
        x1, y1: координаты первой вершины
        color1: цвет первой вершины (tuple RGB)
        x2, y2: координаты второй вершины  
        color2: цвет второй вершины
        x3, y3: координаты третьей вершины
        color3: цвет третьей вершины
    """
    
    # Находим ограничивающий прямоугольник треугольника
    min_x = max(0, min(x1, x2, x3))
    max_x = min(canvas.width - 1, max(x1, x2, x3))
    min_y = max(0, min(y1, y2, y3))
    max_y = min(canvas.height - 1, max(y1, y2, y3))
    
    # Проходим по всем пикселям в ограничивающем прямоугольнике
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # Проверяем, находится ли пиксель внутри треугольника
            if is_point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):
                # Вычисляем barycentric coordinates
                w1, w2, w3 = compute_barycentric_coords(x, y, x1, y1, x2, y2, x3, y3)
                
                # Смешиваем цвета по barycentric coordinates
                r = clamp(int(w1 * color1[0] + w2 * color2[0] + w3 * color3[0]))
                g = clamp(int(w1 * color1[1] + w2 * color2[1] + w3 * color3[1]))
                b = clamp(int(w1 * color1[2] + w2 * color2[2] + w3 * color3[2]))
                
                # Устанавливаем цвет пикселя на холсте
                canvas.set_pixel(x, y, (r, g, b))

def is_point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):
    """
    Проверяет, находится ли точка внутри треугольника используя метод полуплоскостей
    """
    # Вычисляем векторные произведения для проверки ориентации
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign((x, y), (x1, y1), (x2, y2))
    d2 = sign((x, y), (x2, y2), (x3, y3))
    d3 = sign((x, y), (x3, y3), (x1, y1))
    
    # Проверяем, что точка находится по одну сторону от всех сторон
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def compute_barycentric_coords(x, y, x1, y1, x2, y2, x3, y3):
    """
    Вычисляет barycentric coordinates для точки (x, y) в треугольнике
    """
    # Площадь всего треугольника
    area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
    
    if area == 0:
        return 0, 0, 0
    
    # Площади под-треугольников
    area1 = abs((x2 - x) * (y3 - y) - (x3 - x) * (y2 - y))
    area2 = abs((x3 - x) * (y1 - y) - (x1 - x) * (y3 - y))
    area3 = abs((x1 - x) * (y2 - y) - (x2 - x) * (y1 - y))
    
    # Barycentric coordinates
    w1 = area1 / area
    w2 = area2 / area
    w3 = area3 / area
    
    return w1, w2, w3

def clamp(value, min_val=0, max_val=255):
    """Ограничивает значение в диапазоне [min_val, max_val]"""
    return max(min_val, min(value, max_val))

def draw_triangle_outline(canvas, x1, y1, x2, y2, x3, y3, color=(255, 255, 255)):
    """
    Рисует контур треугольника (для визуализации)
    """
    from algorithms.lines.bresenham import bresenham_line
    bresenham_line(canvas, x1, y1, x2, y2, color)
    bresenham_line(canvas, x2, y2, x3, y3, color)
    bresenham_line(canvas, x3, y3, x1, y1, color)