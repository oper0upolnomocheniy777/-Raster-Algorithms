import pygame
import os
from collections import deque

class PatternFill:
    def __init__(self):
        self.name = "Pattern Fill"
        self.pattern = None
    
    def load_pattern(self, filename):
        """Загружает паттерн из файла с подробной отладкой"""
        try:
            # Получаем абсолютные пути ко всем возможным местам
            current_dir = os.path.abspath(os.path.dirname(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
            
            print(f"\n=== ПОИСК ФАЙЛА ПАТТЕРНА ===")
            print(f"Ищем файл: {filename}")
            print(f"Текущая папка: {current_dir}")
            print(f"Корень проекта: {project_root}")
            
            # Список всех возможных мест для поиска
            possible_paths = [
                os.path.join(project_root, filename),                    # В корне проекта
                os.path.join(project_root, "patterns", filename),        # В папке patterns
                os.path.join(current_dir, filename),                     # В папке algorithms/fill
                os.path.join(project_root, "src", filename),             # В папке src
                os.path.join(project_root, "src", "patterns", filename), # В src/patterns
                filename                                                # Текущая рабочая папка
            ]
            
            # Проверяем каждый путь
            found_path = None
            for path in possible_paths:
                print(f"Проверяем: {path}")
                if os.path.exists(path):
                    found_path = path
                    print(f"✅ ФАЙЛ НАЙДЕН: {path}")
                    break
            
            if not found_path:
                print(f"❌ Файл {filename} не найден ни в одном из мест:")
                for path in possible_paths:
                    print(f"   - {path}")
                return False
            
            # Загружаем изображение
            print(f"Загружаем изображение из: {found_path}")
            pattern_surface = pygame.image.load(found_path)
            self.pattern = pattern_surface.convert()
            
            # Получаем информацию о загруженном изображении
            width, height = self.pattern.get_size()
            print(f"✅ ПАТТЕРН УСПЕШНО ЗАГРУЖЕН!")
            print(f"   Размер: {width}x{height} пикселей")
            print(f"   Формат: {self.pattern.get_bytesize()} байт на пиксель")
            
            return True
            
        except pygame.error as e:
            print(f"❌ ОШИБКА PYGAME ПРИ ЗАГРУЗКЕ: {e}")
            return False
        except Exception as e:
            print(f"❌ НЕОЖИДАННАЯ ОШИБКА: {e}")
            return False
    
    def pattern_fill(self, canvas, start_x, start_y, boundary_color=None):
        """Заливка области паттерном из загруженного изображения"""
        if self.pattern is None:
            print("❌ Нет загруженного паттерна! Сначала нажмите P для загрузки.")
            return
        
        print(f"\n=== НАЧИНАЕМ ЗАЛИВКУ ПАТТЕРНОМ ===")
        print(f"Начальная точка: ({start_x}, {start_y})")
        
        width, height = canvas.width, canvas.height
        pattern_width, pattern_height = self.pattern.get_size()
        
        print(f"Размер холста: {width}x{height}")
        print(f"Размер паттерна: {pattern_width}x{pattern_height}")
        
        # Получаем доступ к пикселям холста и паттерна
        canvas_pixels = pygame.surfarray.pixels2d(canvas.surface)
        pattern_pixels = pygame.surfarray.pixels2d(self.pattern)
        
        if boundary_color is None:
            boundary_color = (255, 255, 255)  # белый по умолчанию
        
        boundary_color_int = self._color_to_int(boundary_color)
        background_color_int = canvas_pixels[start_x, start_y]
        
        print(f"Цвет границы: {boundary_color} -> {boundary_color_int}")
        print(f"Цвет фона в начальной точке: {background_color_int}")
        
        # Проверяем, не пытаемся ли залить границу или уже залитую область
        if background_color_int == boundary_color_int:
            print("❌ Начальная точка находится на границе!")
            del canvas_pixels
            del pattern_pixels
            return
        
        stack = deque()
        stack.append((start_x, start_y))
        visited = set()
        filled_pixels = 0
        
        print("Начинаем заливку...")
        
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
                    # Вычисляем координаты в паттерне (циклическое повторение)
                    pattern_x = fill_x % pattern_width
                    pattern_y = y % pattern_height
                    
                    # Берем цвет из паттерна и устанавливаем на холст
                    canvas_pixels[fill_x, y] = pattern_pixels[pattern_x, pattern_y]
                    filled_pixels += 1
            
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
        
        print(f"✅ ЗАЛИВКА ЗАВЕРШЕНА!")
        print(f"   Заполнено пикселей: {filled_pixels}")
        print(f"   Посещено точек: {len(visited)}")
    
    def create_sample_pattern(self):
        """Создает образец паттерна для тестирования"""
        print("\n=== СОЗДАНИЕ ТЕСТОВОГО ПАТТЕРНА ===")
        
        # Создаем поверхность 32x32 пикселя
        pattern = pygame.Surface((32, 32))
        
        # Заливаем фон градиентом
        for y in range(32):
            for x in range(32):
                r = (x * 8) % 256
                g = (y * 8) % 256
                b = (x * y) % 256
                pattern.set_at((x, y), (r, g, b))
        
        # Рисуем красные диагональные линии
        for i in range(0, 32, 4):
            pygame.draw.line(pattern, (255, 0, 0), (i, 0), (0, i), 1)
            pygame.draw.line(pattern, (255, 0, 0), (i, 32), (32, i), 1)
        
        # Рисуем желтые точки в узоре
        for i in range(4, 32, 8):
            for j in range(4, 32, 8):
                pygame.draw.circle(pattern, (255, 255, 0), (i, j), 1)
        
        # Рисуем зеленые квадраты
        for i in range(2, 32, 16):
            for j in range(2, 32, 16):
                pygame.draw.rect(pattern, (0, 255, 0), (i, j, 4, 4))
        
        # Сохраняем в несколько мест чтобы наверняка
        save_locations = [
            "pattern.png",
            "patterns/pattern.png",
            os.path.join("src", "pattern.png"),
            os.path.join("src", "patterns", "pattern.png")
        ]
        
        success_count = 0
        for location in save_locations:
            try:
                # Создаем папку если нужно
                dir_name = os.path.dirname(location)
                if dir_name and not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                    print(f"Создана папка: {dir_name}")
                
                pygame.image.save(pattern, location)
                print(f"✅ Паттерн сохранен: {location}")
                success_count += 1
            except Exception as e:
                print(f"❌ Ошибка сохранения {location}: {e}")
        
        if success_count > 0:
            print(f"Успешно сохранено в {success_count} мест")
            return True
        else:
            print("❌ Не удалось сохранить паттерн ни в одном месте")
            return False
    
    def _color_to_int(self, color):
        """Конвертирует RGB цвет в integer representation"""
        if isinstance(color, tuple) and len(color) >= 3:
            return (color[0] << 16) | (color[1] << 8) | color[2]
        return color
    
    def get_pattern_info(self):
        """Возвращает информацию о загруженном паттерне"""
        if self.pattern is None:
            return "Паттерн не загружен"
        
        width, height = self.pattern.get_size()
        return f"Паттерн {width}x{height} пикселей"