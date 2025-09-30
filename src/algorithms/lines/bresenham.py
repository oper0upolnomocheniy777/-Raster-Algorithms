def bresenham_line(canvas, x1, y1, x2, y2, color):
    """
    Рисует линию алгоритмом Брезенхема
    
    Args:
        canvas: объект холста
        x1, y1: начальная точка
        x2, y2: конечная точка  
        color: цвет линии (R, G, B)
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # Определяем направление
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    x, y = x1, y1
    
    # Основной алгоритм
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            canvas.set_pixel(x, y, color)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            canvas.set_pixel(x, y, color)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    
    canvas.set_pixel(x2, y2, color)