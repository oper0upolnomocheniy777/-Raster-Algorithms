def wu_line(canvas, x1, y1, x2, y2, color):
    """
    Рисует линию алгоритмом Ву (сглаживание)
    
    Args:
        canvas: объект холста
        x1, y1: начальная точка
        x2, y2: конечная точка
        color: цвет линии (R, G, B)
    """
    def plot(x, y, brightness):
        """Рисует пиксель с прозрачностью"""
        r, g, b = color
        # Смешиваем цвет с фоном (предполагаем черный фон)
        blended_color = (
            int(r * brightness),
            int(g * brightness), 
            int(b * brightness)
        )
        canvas.set_pixel(int(x), int(y), blended_color)
    
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) > abs(dy):
        # Горизонтальная линия
        if x2 < x1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        gradient = dy / dx if dx != 0 else 1
        y = y1
        
        for x in range(int(x1), int(x2) + 1):
            plot(x, int(y), 1 - (y - int(y)))
            plot(x, int(y) + 1, y - int(y))
            y += gradient
    else:
        # Вертикальная линия
        if y2 < y1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        gradient = dx / dy if dy != 0 else 1
        x = x1
        
        for y in range(int(y1), int(y2) + 1):
            plot(int(x), y, 1 - (x - int(x)))
            plot(int(x) + 1, y, x - int(x))
            x += gradient