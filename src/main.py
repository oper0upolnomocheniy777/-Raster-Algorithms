import pygame
import sys
from core.canvas import Canvas
from algorithms.lines.bresenham import bresenham_line
from algorithms.lines.wu import wu_line

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

def draw_interface():
    """Рисует интерфейс"""
    font = pygame.font.SysFont(None, 24)
    
    # Отображаем текущий алгоритм
    algo_text = f"Algorithm: {current_algorithm.upper()}"
    text_surface = font.render(algo_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    # Инструкция
    instr_text = "Click and drag to draw lines. Press SPACE to switch algorithms."
    instr_surface = font.render(instr_text, True, (200, 200, 200))
    screen.blit(instr_surface, (10, HEIGHT - 30))

def main():
    # Объявляем global ПЕРЕД использованием
    global drawing, start_pos, current_algorithm, line_color
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    drawing = True
                    start_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
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
                    # Переключаем алгоритм
                    current_algorithm = "wu" if current_algorithm == "bresenham" else "bresenham"
                elif event.key == pygame.K_c:
                    # Очищаем холст
                    canvas.clear()
                elif event.key == pygame.K_1:
                    # Смена цвета на красный
                    line_color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    # Смена цвета на зеленый
                    line_color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    # Смена цвета на синий
                    line_color = (0, 0, 255)
        
        # Отрисовка
        screen.fill((0, 0, 0))  # Черный фон
        canvas.draw_to_screen(screen)
        draw_interface()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()